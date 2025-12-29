// Transaction type based on blockchain structure
export interface Transaction {
  sender: string;
  recipient: string;
  amount: number;
  timestamp: string;
  purpose?: string;
  approved_by?: string;
  block_id?: string;
  validator?: string;
}

// Block type from blockchain
export interface Block {
  block_id: string;
  timestamp: string;
  transactions: Transaction[];
  previous_hash: string;
  hash: string;
  validator: string;
}

// Blockchain response
export interface Blockchain {
  chain: Block[];
  length: number;
}

// Report types
export interface Report {
  id: number;
  report_type: 'citizen_portal' | 'tax_payment';
  reported_by: string;
  subject: string;
  description: string;
  transaction_hash?: string;
  status: 'pending' | 'reviewed' | 'resolved';
  created_at: string;
  reviewed_by?: string;
  admin_notes?: string;
}

// User/Auth types
export interface User {
  office_name: string;
  wallet_address: string;
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// Statistics for dashboard
export interface TransactionStats {
  totalTransactions: number;
  totalFunds: number;
  activeOffices: number;
}
