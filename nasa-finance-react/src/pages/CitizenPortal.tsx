import { useState, useEffect } from 'react';
import { format } from 'date-fns';
import DOMPurify from 'dompurify';
import { blockchainAPI } from '../services/api';
import type { Transaction, TransactionStats } from '../types';

export default function CitizenPortal() {
  const [allTransactions, setAllTransactions] = useState<Transaction[]>([]);
  const [displayedTransactions, setDisplayedTransactions] = useState<Transaction[]>([]);
  const [stats, setStats] = useState<TransactionStats>({
    totalTransactions: 0,
    totalFunds: 0,
    activeOffices: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  
  // Filter states
  const [searchPurpose, setSearchPurpose] = useState('');
  const [amountFilter, setAmountFilter] = useState('all');

  // Load blockchain data
  const loadBlockchainData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const blockchain = await blockchainAPI.getBlockchain();
      
      // Extract all transactions from all blocks
      const transactions: Transaction[] = [];
      let totalFunds = 0;
      const uniqueAddresses = new Set<string>();

      blockchain.chain.forEach(block => {
        if (block.transactions && block.transactions.length > 0) {
          block.transactions.forEach(tx => {
            transactions.push({
              ...tx,
              timestamp: block.timestamp,
              block_id: block.block_id,
              validator: block.validator,
            });
            totalFunds += parseFloat(String(tx.amount || 0));
            uniqueAddresses.add(tx.sender);
            uniqueAddresses.add(tx.recipient);
          });
        }
      });

      setAllTransactions(transactions);
      setDisplayedTransactions(transactions);
      setStats({
        totalTransactions: transactions.length,
        totalFunds,
        activeOffices: uniqueAddresses.size,
      });
      setLastUpdate(new Date());
      setLoading(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load blockchain data');
      setLoading(false);
    }
  };

  // Filter transactions
  const filterTransactions = () => {
    let filtered = [...allTransactions];

    // Filter by purpose
    if (searchPurpose) {
      const searchLower = searchPurpose.toLowerCase();
      filtered = filtered.filter(tx =>
        (tx.purpose || '').toLowerCase().includes(searchLower) ||
        (tx.approved_by || '').toLowerCase().includes(searchLower)
      );
    }

    // Filter by amount
    if (amountFilter !== 'all') {
      filtered = filtered.filter(tx => {
        const amount = parseFloat(String(tx.amount));
        if (amountFilter === '0-1000') return amount < 1000;
        if (amountFilter === '1000-10000') return amount >= 1000 && amount < 10000;
        if (amountFilter === '10000+') return amount >= 10000;
        return true;
      });
    }

    setDisplayedTransactions(filtered);
  };

  // Format date
  const formatDate = (timestamp: string) => {
    return format(new Date(timestamp), 'MMM dd, yyyy HH:mm');
  };

  // Truncate wallet address
  const truncateAddress = (address: string) => {
    if (!address) return 'N/A';
    return `${address.substring(0, 8)}...${address.substring(address.length - 6)}`;
  };

  // Sanitize user content
  const sanitize = (content: string) => {
    return DOMPurify.sanitize(content);
  };

  // Initial load and auto-refresh
  useEffect(() => {
    loadBlockchainData();
    const interval = setInterval(loadBlockchainData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  // Apply filters when they change
  useEffect(() => {
    filterTransactions();
  }, [searchPurpose, amountFilter, allTransactions]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-600 to-green-800 text-white py-6 px-6 shadow-lg">
        <div className="container mx-auto">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold flex items-center gap-2">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
                </svg>
                Citizen Finance Tracker
              </h1>
              <p className="text-sm text-green-100 mt-1">Transparent Public Finance Monitoring System</p>
            </div>
            <div className="text-right">
              <p className="text-xs text-green-200">Powered by Blockchain Technology</p>
              <p className="text-sm font-semibold">
                <svg className="w-4 h-4 inline mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                </svg>
                100% Transparent
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Info Banner */}
        <div className="bg-blue-50 border-l-4 border-blue-400 p-4 mb-6 rounded-r-lg">
          <div className="flex items-center">
            <svg className="w-5 h-5 text-blue-400 mr-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
            <p className="text-sm text-blue-700">
              <strong>Public Access:</strong> View all government financial transactions in real-time. 
              All data is secured and verified on the blockchain.
            </p>
          </div>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="stat-card bg-white rounded-lg shadow-md p-6 transition-transform hover:-translate-y-1">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm uppercase">Total Transactions</p>
                <p className="text-3xl font-bold text-gray-800 mt-2">{stats.totalTransactions}</p>
              </div>
              <div className="bg-blue-100 p-4 rounded-full">
                <svg className="w-8 h-8 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M8 5a1 1 0 100 2h5.586l-1.293 1.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L13.586 5H8zM12 15a1 1 0 100-2H6.414l1.293-1.293a1 1 0 10-1.414-1.414l-3 3a1 1 0 000 1.414l3 3a1 1 0 001.414-1.414L6.414 15H12z" />
                </svg>
              </div>
            </div>
          </div>

          <div className="stat-card bg-white rounded-lg shadow-md p-6 transition-transform hover:-translate-y-1">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm uppercase">Total Funds Moved</p>
                <p className="text-3xl font-bold text-gray-800 mt-2">{stats.totalFunds.toFixed(2)}</p>
              </div>
              <div className="bg-green-100 p-4 rounded-full">
                <svg className="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z" />
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
          </div>

          <div className="stat-card bg-white rounded-lg shadow-md p-6 transition-transform hover:-translate-y-1">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm uppercase">Active Offices</p>
                <p className="text-3xl font-bold text-gray-800 mt-2">{stats.activeOffices}</p>
              </div>
              <div className="bg-purple-100 p-4 rounded-full">
                <svg className="w-8 h-8 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2h-3a1 1 0 01-1-1v-2a1 1 0 00-1-1H9a1 1 0 00-1 1v2a1 1 0 01-1 1H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clipRule="evenodd" />
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Search and Filter */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label htmlFor="searchPurpose" className="block text-sm font-medium text-gray-700 mb-2">
                Search by Purpose
              </label>
              <input
                type="text"
                id="searchPurpose"
                placeholder="e.g., Education, Healthcare..."
                value={searchPurpose}
                onChange={(e) => setSearchPurpose(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
              />
            </div>
            <div>
              <label htmlFor="filterAmount" className="block text-sm font-medium text-gray-700 mb-2">
                Filter by Amount
              </label>
              <select
                id="filterAmount"
                value={amountFilter}
                onChange={(e) => setAmountFilter(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500"
              >
                <option value="all">All Amounts</option>
                <option value="0-1000">Under 1,000</option>
                <option value="1000-10000">1,000 - 10,000</option>
                <option value="10000+">Above 10,000</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={filterTransactions}
                className="w-full px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                <svg className="w-4 h-4 inline mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
                </svg>
                Search
              </button>
            </div>
          </div>
        </div>

        {/* Transactions Table */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="px-6 py-4 bg-gray-50 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
              </svg>
              Public Finance Transactions
            </h2>
            <p className="text-sm text-gray-600 mt-1">
              All government financial activities · Last updated: {format(lastUpdate, 'MMM dd, yyyy HH:mm:ss')}
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200">
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date & Time</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">From Office</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">To Office</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Purpose</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Approved By</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 bg-white">
                {loading ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-8 text-center text-gray-500">
                      <svg className="animate-spin h-8 w-8 mx-auto mb-2 text-gray-400" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <p>Loading public transactions...</p>
                    </td>
                  </tr>
                ) : error ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-8 text-center text-red-500">
                      <svg className="w-12 h-12 mx-auto mb-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                      <p>Error loading transactions: {sanitize(error)}</p>
                      <button
                        onClick={loadBlockchainData}
                        className="mt-4 px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                      >
                        Retry
                      </button>
                    </td>
                  </tr>
                ) : displayedTransactions.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-8 text-center text-gray-500">
                      <svg className="w-16 h-16 mx-auto mb-3 text-gray-300" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M5 2a2 2 0 00-2 2v14l3.5-2 3.5 2 3.5-2 3.5 2V4a2 2 0 00-2-2H5zm2.5 3a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm6.207.293a1 1 0 00-1.414 0l-6 6a1 1 0 101.414 1.414l6-6a1 1 0 000-1.414zM12.5 10a1.5 1.5 0 100 3 1.5 1.5 0 000-3z" clipRule="evenodd" />
                      </svg>
                      <p>No transactions found</p>
                    </td>
                  </tr>
                ) : (
                  [...displayedTransactions]
                    .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
                    .map((tx, index) => (
                      <tr key={index} className="hover:bg-gray-50 transition-colors">
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {formatDate(tx.timestamp)}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">
                          <code className="bg-gray-100 px-2 py-1 rounded text-xs">
                            {truncateAddress(tx.sender)}
                          </code>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">
                          <code className="bg-gray-100 px-2 py-1 rounded text-xs">
                            {truncateAddress(tx.recipient)}
                          </code>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-green-600">
                          {parseFloat(String(tx.amount)).toFixed(2)}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          <span dangerouslySetInnerHTML={{ __html: sanitize(tx.purpose || 'Not specified') }} />
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">
                          <span dangerouslySetInnerHTML={{ __html: sanitize(tx.approved_by || 'Not specified') }} />
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                            <svg className="w-3 h-3 inline mr-1" fill="currentColor" viewBox="0 0 20 20">
                              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            Verified
                          </span>
                        </td>
                      </tr>
                    ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 text-center text-gray-600 text-sm">
          <p>
            <strong>Transparency Notice:</strong> This portal displays real-time government transactions from the blockchain. 
            All transactions are immutable and verified by validators.
          </p>
          <p className="mt-2">
            Last blockchain update: {format(lastUpdate, 'PPpp')}
          </p>
        </div>
      </div>
    </div>
  );
}
