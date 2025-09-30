#[allow(unreachable_pub)]
use borsh::{BorshDeserialize, BorshSerialize, to_vec};
use solana_sdk::{
    pubkey::Pubkey,
    signature::{Keypair, Signer},
};

/// Time in Force order types
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq, Default)]
pub(crate) enum TimeInForce {
    /// Immediate or Cancel - execute immediately, cancel remainder
    IOC,
    /// Fill or Kill - execute completely or cancel entirely  
    FOK,
    /// Good Till Cancelled - remain active until cancelled
    #[default]
    GTC,
    /// Add Liquidity Only - only place if order rests
    ALO,
    /// Good Till Time - remain active until specified timestamp
    GTT(u64),
}

/// Domain separator for permit verification
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub(crate) struct PermitDomain {
    pub(crate) program_id: Pubkey,
    pub(crate) cluster: ClusterType,
    pub(crate) version: u8,
}

#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, Copy, PartialEq)]
pub(crate) enum ClusterType {
    Mainnet,
    Testnet,
    Devnet,
    Localnet,
}

/// Replay prevention mode
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub(crate) enum ReplayMode {
    Sequence(u64),
    Nonce([u8; 32]),
    Allowance([u8; 32]),
    HlWindow { k: u8 },
}

/// Stored sequence replay state
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, Default)]
pub(crate) struct SequenceState {
    pub(crate) next_sequence: u64,
    pub(crate) bump: u8,
}

impl SequenceState {
    pub(crate) const LEN: usize = 8 + 1;
}

/// Health floor specification
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub(crate) struct HealthFloor {
    pub(crate) metric: HealthMetric,
    pub(crate) min: i64,
}

#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub(crate) enum HealthMetric {
    Initial,
    Maintenance,
    RatioBps,
}

/// Permit action variants
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub(crate) enum PermitAction {
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
        to_owner: Pubkey,
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
        recipient: Pubkey,
    },
}

/// Main permit envelope structure (V1)
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone)]
pub(crate) struct PermitEnvelopeV1 {
    pub(crate) domain: PermitDomain,
    pub(crate) authorizer: Pubkey,
    pub(crate) key_type: KeyType,
    pub(crate) action: PermitAction,
    pub(crate) mode: ReplayMode,
    pub(crate) expires_unix: i64,
    pub(crate) max_fee_quote: u64,
    pub(crate) relayer: Option<Pubkey>,
    pub(crate) nonce: u64,
}

#[derive(BorshSerialize, BorshDeserialize, Debug, Clone, PartialEq)]
pub(crate) enum KeyType {
    Ed25519,
    Secp256k1,
}

/// Session PDA state
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone)]
pub(crate) struct SessionState {
    pub(crate) owner: Pubkey,
    pub(crate) session: Pubkey,
    pub(crate) expires_unix: i64,
    pub(crate) scopes_bits: u32,
    pub(crate) withdraw_limit_24h: u64,
    pub(crate) per_market_size_limit_lots: i64,
    pub(crate) bump: u8,
}

impl SessionState {
    pub(crate) const LEN: usize = 32 + 32 + 8 + 4 + 8 + 8 + 1;

    pub(crate) fn has_scope(&self, action: &PermitAction) -> bool {
        match action {
            PermitAction::Place { .. } => (self.scopes_bits & SCOPE_PLACE) != 0,
            PermitAction::CancelById { .. }
            | PermitAction::CancelByClientId { .. }
            | PermitAction::CancelAll { .. } => (self.scopes_bits & SCOPE_CANCEL) != 0,
            PermitAction::Modify { .. } => {
                (self.scopes_bits & SCOPE_CANCEL) != 0 && (self.scopes_bits & SCOPE_PLACE) != 0
            }
            PermitAction::Withdraw { .. } => (self.scopes_bits & SCOPE_WITHDRAW) != 0,
            PermitAction::SetLeverage { .. } => (self.scopes_bits & SCOPE_SET_LEVERAGE) != 0,
            PermitAction::Faucet { .. } => (self.scopes_bits & SCOPE_FAUCET) != 0,
            PermitAction::Noop => true,
        }
    }
}

pub(crate) const SCOPE_PLACE: u32 = 1 << 0;
pub(crate) const SCOPE_CANCEL: u32 = 1 << 1;
pub(crate) const SCOPE_WITHDRAW: u32 = 1 << 2;
pub(crate) const SCOPE_SET_LEVERAGE: u32 = 1 << 3;
pub(crate) const SCOPE_FAUCET: u32 = 1 << 4;

/// Allowance PDA state
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone)]
pub(crate) struct AllowanceState {
    pub(crate) owner: Pubkey,
    pub(crate) session: Pubkey,
    pub(crate) id: [u8; 32],
    pub(crate) remaining_uses: u32,
    pub(crate) expires_unix: i64,
    pub(crate) scopes_bits: u32,
    pub(crate) bump: u8,
}

impl AllowanceState {
    pub(crate) const LEN: usize = 32 + 32 + 32 + 4 + 8 + 4 + 1;
}

/// Used nonce PDA state (minimal marker)
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone)]
pub(crate) struct UsedNonceState {
    pub(crate) timestamp: i64,
    pub(crate) bump: u8,
}

impl UsedNonceState {
    pub(crate) const LEN: usize = 8 + 1;
}

/// Nonce window PDA state (Hyperliquid-style window)
#[derive(BorshSerialize, BorshDeserialize, Debug, Clone)]
pub(crate) struct NonceWindowState {
    pub(crate) signer: Pubkey,
    pub(crate) k: u8,
    pub(crate) top: Vec<u64>,
    pub(crate) bump: u8,
}

impl NonceWindowState {
    pub(crate) const MAX_K: u8 = 128;
    pub(crate) const LEN: usize = 32 + 1 + 4 + ((Self::MAX_K as usize) * 8) + 1; // Max size with k=128

    pub(crate) fn insert_nonce(&mut self, nonce: u64) -> Result<(), &'static str> {
        if self.top.contains(&nonce) {
            return Err("Nonce already used");
        }

        if self.top.len() < self.k as usize {
            self.top.push(nonce);
            self.top.sort_unstable();
            return Ok(());
        }

        let smallest = self.top[0];
        if nonce <= smallest {
            return Err("Nonce too small for window");
        }

        self.top[0] = nonce;
        self.top.sort_unstable();
        Ok(())
    }

    pub(crate) fn is_valid_nonce(&self, nonce: u64, now_ms: i64) -> bool {
        let two_days_ms = 2 * 24 * 60 * 60 * 1000;
        let one_day_ms = 24 * 60 * 60 * 1000;

        let nonce_time = nonce as i64;
        if nonce_time < (now_ms - two_days_ms) || nonce_time > (now_ms + one_day_ms) {
            return false;
        }

        true
    }
}

/// Event emitted when a permit is consumed
#[derive(BorshSerialize, BorshDeserialize, Debug)]
pub(crate) struct PermitConsumedEvent {
    pub(crate) owner: Pubkey,
    pub(crate) authorizer: Pubkey,
    pub(crate) action_hash: [u8; 32],
    pub(crate) nonce: u64,
    pub(crate) timestamp: i64,
}

/// Result of signing a permit envelope with an Ed25519 keypair.
#[derive(Debug, Clone, PartialEq, Eq)]
pub(crate) struct SignedPermit {
    pub(crate) bytes: Vec<u8>,
    pub(crate) signature: [u8; 64],
}

impl SignedPermit {
    pub(crate) fn into_parts(self) -> (Vec<u8>, [u8; 64]) {
        (self.bytes, self.signature)
    }
}

/// Serialize and sign a permit envelope with the provided Ed25519 keypair.
pub(crate) fn sign_permit_ed25519(
    envelope: &PermitEnvelopeV1,
    keypair: &Keypair,
) -> Result<SignedPermit, std::io::Error> {
    let bytes = to_vec(&envelope)?;
    let signature = keypair.sign_message(&bytes).into();
    Ok(SignedPermit { bytes, signature })
}

#[cfg(test)]
mod tests {
    use super::*;

    use solana_sdk::{pubkey, signature::Signature, signer::SeedDerivable};

    #[test]
    fn test_nonce_window_insert() {
        let mut window = NonceWindowState {
            signer: Pubkey::new_unique(),
            k: 3,
            top: vec![],
            bump: 0,
        };

        assert!(window.insert_nonce(100).is_ok());
        assert_eq!(window.top, vec![100]);

        assert!(window.insert_nonce(200).is_ok());
        assert_eq!(window.top, vec![100, 200]);

        assert!(window.insert_nonce(150).is_ok());
        assert_eq!(window.top, vec![100, 150, 200]);

        assert!(window.insert_nonce(300).is_ok());
        assert_eq!(window.top, vec![150, 200, 300]);

        assert!(window.insert_nonce(140).is_err());
        assert_eq!(window.top, vec![150, 200, 300]);

        assert!(window.insert_nonce(200).is_err());
        assert_eq!(window.top, vec![150, 200, 300]);
    }

    #[test]
    fn test_nonce_window_time_bounds() {
        let window = NonceWindowState {
            signer: Pubkey::new_unique(),
            k: 128,
            top: vec![],
            bump: 0,
        };

        let now_ms: i64 = 1_700_000_000_000;
        let one_day_ms = 24 * 60 * 60 * 1000;
        let two_days_ms = 2 * one_day_ms;

        assert!(window.is_valid_nonce(now_ms as u64, now_ms));
        assert!(window.is_valid_nonce((now_ms - one_day_ms) as u64, now_ms));
        assert!(window.is_valid_nonce((now_ms + (one_day_ms / 2)) as u64, now_ms));

        assert!(!window.is_valid_nonce((now_ms - two_days_ms - 1000) as u64, now_ms));
        assert!(!window.is_valid_nonce((now_ms + one_day_ms + 1000) as u64, now_ms));
    }

    #[test]
    fn test_session_has_scope() {
        let session = SessionState {
            owner: Pubkey::new_unique(),
            session: Pubkey::new_unique(),
            expires_unix: 0,
            scopes_bits: SCOPE_PLACE | SCOPE_CANCEL,
            withdraw_limit_24h: 0,
            per_market_size_limit_lots: 0,
            bump: 0,
        };

        assert!(session.has_scope(&PermitAction::Place {
            market_id: 1,
            client_id: 123,
            side: 0,
            qty: 100,
            price: Some(1000),
            tif: TimeInForce::GTC,
            reduce_only: false,
            trigger_price: None,
            trigger_type: 0,
            health_floor: None,
        }));

        assert!(session.has_scope(&PermitAction::CancelById {
            market_id: 1,
            order_id: 123,
        }));

        assert!(!session.has_scope(&PermitAction::Withdraw {
            amount: 1000,
            to_owner: Pubkey::new_unique(),
            health_floor: None,
        }));

        assert!(!session.has_scope(&PermitAction::SetLeverage {
            market_id: 1,
            target_leverage_bps: 200,
            health_floor: None,
        }));

        assert!(!session.has_scope(&PermitAction::Faucet {
            market_id: 1,
            amount: 1_000,
            recipient: Pubkey::new_unique(),
        }));

        let faucet_session = SessionState {
            scopes_bits: SCOPE_FAUCET,
            ..session.clone()
        };
        assert!(faucet_session.has_scope(&PermitAction::Faucet {
            market_id: 1,
            amount: 1_000,
            recipient: Pubkey::new_unique(),
        }));
    }

    #[test]
    fn test_permit_envelope_serialization() {
        let envelope = PermitEnvelopeV1 {
            domain: PermitDomain {
                program_id: Pubkey::new_unique(),
                cluster: ClusterType::Testnet,
                version: 1,
            },
            authorizer: Pubkey::new_unique(),
            key_type: KeyType::Ed25519,
            action: PermitAction::Place {
                market_id: 1,
                client_id: 12345,
                side: 0,
                qty: 100,
                price: Some(50000),
                tif: TimeInForce::GTC,
                reduce_only: false,
                trigger_price: None,
                trigger_type: 0,
                health_floor: None,
            },
            mode: ReplayMode::HlWindow { k: 128 },
            expires_unix: 1700000000,
            max_fee_quote: 0,
            relayer: None,
            nonce: 123456789,
        };

        let serialized = to_vec(&envelope).unwrap();
        let deserialized = PermitEnvelopeV1::try_from_slice(&serialized).unwrap();

        assert_eq!(envelope.domain.version, deserialized.domain.version);
        assert_eq!(envelope.authorizer, deserialized.authorizer);
        assert_eq!(envelope.nonce, deserialized.nonce);
        assert_eq!(envelope.expires_unix, deserialized.expires_unix);
    }

    #[test]
    fn test_health_floor_variants() {
        let floor1 = HealthFloor {
            metric: HealthMetric::Initial,
            min: 0,
        };

        let floor2 = HealthFloor {
            metric: HealthMetric::Maintenance,
            min: 1000,
        };

        let floor3 = HealthFloor {
            metric: HealthMetric::RatioBps,
            min: 150,
        };

        assert!(to_vec(&floor1).is_ok());
        assert!(to_vec(&floor2).is_ok());
        assert!(to_vec(&floor3).is_ok());
    }

    #[test]
    fn test_sign_permit_ed25519() {
        let secret_key = [7u8; 32];
        let keypair = Keypair::from_seed(&secret_key).unwrap();

        let envelope = PermitEnvelopeV1 {
            domain: PermitDomain {
                program_id: Pubkey::new_unique(),
                cluster: ClusterType::Testnet,
                version: 1,
            },
            authorizer: Pubkey::new_unique(),
            key_type: KeyType::Ed25519,
            action: PermitAction::Noop,
            mode: ReplayMode::HlWindow { k: 16 },
            expires_unix: 1_700_000_000,
            max_fee_quote: 0,
            relayer: None,
            nonce: 42,
        };

        let signed = sign_permit_ed25519(&envelope, &keypair).expect("signing should succeed");
        assert_eq!(signed.bytes, to_vec(&envelope).unwrap());

        let expected: [u8; 64] = keypair.sign_message(&signed.bytes).into();
        assert_eq!(signed.signature, expected);
    }

    #[test]
    fn test_known_signature() {
        let secret_key: [u8; 64] = [20,203,107,91,91,213,103,76,93,63,148,48,107,244,68,66,228,29,223,229,232,131,244,13,37,11,53,94,105,124,18,186,62,104,91,218,112,209,229,196,207,142,233,157,74,69,251,215,76,5,120,105,25,128,52,86,101,30,18,64,121,208,167,120];
        let keypair = Keypair::from_seed(&secret_key).unwrap();

        let envelope = PermitEnvelopeV1 {
            domain: PermitDomain {
                program_id: pubkey!("6egfvA3boGA8BLTgCzwPfKZMv3W9QS5V61Ewqa6VWq2g"),
                cluster: ClusterType::Testnet,
                version: 1,
            },
            authorizer: pubkey!("5CcaDcVkVusXtPndVX8Hi4Wi68iw2hE6r6xcRmZ5NirK"),
            key_type: KeyType::Ed25519,
            action: PermitAction::Place {
                market_id: 64,
                client_id: 3748278,
                side: 0,
                qty: 10000,
                price: Some(75000000000),
                tif: TimeInForce::GTC,
                reduce_only: false,
                trigger_price: None,
                trigger_type: 0,
                health_floor: None,
            },
            mode: ReplayMode::HlWindow { k: 128 },
            expires_unix: 1758803887,
            max_fee_quote: 1000000,
            nonce: 1758803827331,
            relayer: None,
        };

        println!("Envelope: {:?}", to_vec(&envelope).unwrap());
        let signed = sign_permit_ed25519(&envelope, &keypair).unwrap();
        let signature = hex::encode(signed.signature);
        println!("Signed: {}", signature);
    }

}