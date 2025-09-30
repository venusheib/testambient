use pyo3::prelude::*;
use borsh::{BorshDeserialize, BorshSerialize, to_vec};
use ed25519_dalek::{Keypair, Signer};

/// Time in Force order types
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub enum TimeInForce {
    /// Immediate or Cancel - execute immediately, cancel remainder
    IOC,
    /// Fill or Kill - execute completely or cancel entirely  
    FOK,
    /// Good Till Cancelled - remain active until cancelled
    GTC,
    /// Add Liquidity Only - only place if order rests
    ALO,
    /// Good Till Time - remain active until specified timestamp
    GTT(u64),
}

impl Default for TimeInForce {
    fn default() -> Self {
        TimeInForce::GTC
    }
}

/// Domain separator for permit verification
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub struct PermitDomain {
    pub program_id: [u8; 32],
    pub cluster: ClusterType,
    pub version: u8,
}

#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, Copy, PartialEq)]
pub enum ClusterType {
    Mainnet,
    Testnet,
    Devnet,
    Localnet,
}

/// Replay prevention mode
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub enum ReplayMode {
    Sequence(u64),
    Nonce([u8; 32]),
    Allowance([u8; 32]),
    HlWindow { k: u8 },
}

/// Health floor specification
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub struct HealthFloor {
    pub metric: HealthMetric,
    pub min: i64,
}

#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub enum HealthMetric {
    Initial,
    Maintenance,
    RatioBps,
}

/// Permit action variants
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub enum PermitAction {
    Place {
        market_id: u64,
        client_id: u128,
        side: u8,
        qty: u64,
        price: Option<u64>,
        tif: TimeInForce,
        reduce_only: bool,
        trigger_price: Option<u64>,
        trigger_type: u8,
        health_floor: Option<HealthFloor>,
    },
    CancelById {
        market_id: u64,
        order_id: u64,
    },
    CancelByClientId {
        market_id: u64,
        client_id: u128,
    },
    CancelAll {
        market_id: Option<u64>,
    },
    Modify {
        market_id: u64,
        cancel_order_id: u64,
        new_client_id: u128,
        side: u8,
        qty: u64,
        price: Option<u64>,
        tif: TimeInForce,
        reduce_only: bool,
        trigger_price: Option<u64>,
        trigger_type: u8,
        health_floor: Option<HealthFloor>,
    },
    Withdraw {
        amount: u64,
        to_owner: [u8; 32],
        health_floor: Option<HealthFloor>,
    },
    SetLeverage {
        market_id: u64,
        target_leverage_bps: u16,
        health_floor: Option<HealthFloor>,
    },
    Noop,
    Faucet {
        market_id: u64,
        amount: u64,
        recipient: [u8; 32],
    },
}

#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub enum KeyType {
    Ed25519,
    Secp256k1,
}

/// Main permit envelope structure (V1)
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone)]
pub struct PermitEnvelopeV1 {
    pub domain: PermitDomain,
    pub authorizer: [u8; 32],
    pub key_type: KeyType,
    pub action: PermitAction,
    pub mode: ReplayMode,
    pub expires_unix: i64,
    pub max_fee_quote: u64,
    pub relayer: Option<[u8; 32]>,
    pub nonce: u64,
}

/// Result of signing a permit envelope with an Ed25519 keypair.
#[derive(Debug, Clone, PartialEq, Eq)]
#[pyclass]
pub struct SignedPermit {
    #[pyo3(get)]
    pub bytes: Vec<u8>,
    #[pyo3(get)]
    pub signature: Vec<u8>,
}

#[pymethods]
impl SignedPermit {
    #[getter]
    fn signature_hex(&self) -> String {
        hex::encode(&self.signature)
    }
    
    #[getter]
    fn bytes_hex(&self) -> String {
        hex::encode(&self.bytes)
    }
}

/// Serialize and sign a permit envelope with the provided Ed25519 keypair.
fn sign_permit_ed25519(
    envelope: &PermitEnvelopeV1,
    keypair: &Keypair,
) -> Result<SignedPermit, std::io::Error> {
    let bytes = to_vec(&envelope)?;
    let signature = keypair.sign(&bytes);
    Ok(SignedPermit { 
        bytes, 
        signature: signature.to_bytes().to_vec()
    })
}

fn parse_pubkey(pubkey_str: &str) -> Result<[u8; 32], String> {
    // Handle both hex and base58 formats
    if pubkey_str.len() == 64 {
        // Hex format
        let decoded = hex::decode(pubkey_str)
            .map_err(|e| format!("Invalid hex pubkey: {}", e))?;
        if decoded.len() != 32 {
            return Err("Hex pubkey must be 32 bytes".to_string());
        }
        let mut result = [0u8; 32];
        result.copy_from_slice(&decoded);
        Ok(result)
    } else if pubkey_str.len() == 44 || pubkey_str.len() == 43 {
        // Base58 format (Solana standard)
        let decoded = bs58::decode(pubkey_str)
            .into_vec()
            .map_err(|e| format!("Invalid base58 pubkey: {}", e))?;
        if decoded.len() != 32 {
            return Err("Base58 pubkey must decode to 32 bytes".to_string());
        }
        let mut result = [0u8; 32];
        result.copy_from_slice(&decoded);
        Ok(result)
    } else {
        Err(format!("Invalid pubkey length: {} (expected 44 for base58 or 64 for hex)", pubkey_str.len()))
    }
}

/// Python-callable ambient signer
#[pyclass]
pub struct AmbientSigner {
    keypair: Keypair,
}

#[pymethods]
impl AmbientSigner {
    #[new]
    fn new(private_key_bytes: Vec<u8>) -> PyResult<Self> {
        if private_key_bytes.len() != 64 {
            return Err(pyo3::exceptions::PyValueError::new_err(
                "Private key must be 64 bytes"
            ));
        }

        let keypair = Keypair::from_bytes(&private_key_bytes)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid private key: {}", e)))?;
        
        Ok(AmbientSigner { keypair })
    }
    
    #[staticmethod]
    fn from_hex(hex_str: &str) -> PyResult<Self> {
        let bytes = hex::decode(hex_str)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid hex: {}", e)))?;
        Self::new(bytes)
    }
    
    #[getter]
    fn public_key(&self) -> String {
        bs58::encode(self.keypair.public.as_bytes()).into_string()
    }
    
    #[getter]
    fn public_key_hex(&self) -> String {
        hex::encode(self.keypair.public.as_bytes())
    }
    
    fn sign_place_order(
        &self,
        program_id: &str,
        cluster: &str,
        authorizer: &str,
        market_id: u64,
        client_id: u128,
        side: u8,
        qty: u64,
        expires_unix: i64,
        max_fee_quote: u64,
        nonce: u64,
        price: Option<u64>,
        tif: Option<&str>,
        reduce_only: Option<bool>,
        trigger_price: Option<u64>,
        trigger_type: Option<u8>,
        relayer: Option<&str>,
    ) -> PyResult<SignedPermit> {
        let program_id = parse_pubkey(program_id)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid program_id: {}", e)))?;
        
        let authorizer = parse_pubkey(authorizer)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid authorizer: {}", e)))?;
        
        let cluster = match cluster {
            "mainnet" => ClusterType::Mainnet,
            "testnet" => ClusterType::Testnet,
            "devnet" => ClusterType::Devnet,
            "localnet" => ClusterType::Localnet,
            _ => return Err(pyo3::exceptions::PyValueError::new_err("Invalid cluster type")),
        };
        
        let tif = match tif.unwrap_or("Gtc") {
            "IOC" | "Ioc" => TimeInForce::IOC,
            "FOK" | "Fok" => TimeInForce::FOK,
            "GTC" | "Gtc" => TimeInForce::GTC,
            "ALO" | "Alo" => TimeInForce::ALO,
            _ => return Err(pyo3::exceptions::PyValueError::new_err("Invalid time in force")),
        };
        
        let reduce_only = reduce_only.unwrap_or(false);
        let trigger_type = trigger_type.unwrap_or(0);
        
        let relayer = if let Some(rel) = relayer {
            Some(parse_pubkey(rel)
                .map_err(|e| pyo3::exceptions::PyValueError::new_err(format!("Invalid relayer: {}", e)))?)
        } else {
            None
        };
        
        let envelope = PermitEnvelopeV1 {
            domain: PermitDomain {
                program_id,
                cluster,
                version: 1,
            },
            authorizer,
            key_type: KeyType::Ed25519,
            action: PermitAction::Place {
                market_id,
                client_id,
                side,
                qty,
                price,
                tif,
                reduce_only,
                trigger_price,
                trigger_type,
                health_floor: None,
            },
            mode: ReplayMode::HlWindow { k: 128 },
            expires_unix,
            max_fee_quote,
            relayer,
            nonce,
        };
        
        sign_permit_ed25519(&envelope, &self.keypair)
            .map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(format!("Signing failed: {}", e)))
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn ambient_signer(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<AmbientSigner>()?;
    m.add_class::<SignedPermit>()?;
    Ok(())
}