import { useState } from 'react';

const PRESETS = [10, 20, 50, 100];

const AmountSelector = ({ onSelect }) => {
  const [customAmount, setCustomAmount] = useState('');
  const [error, setError] = useState('');

  const handleCustomSubmit = (e) => {
    e.preventDefault();
    const val = parseFloat(customAmount);
    if (!val || val < 2) {
      setError('Minimum tip is K2');
      return;
    }
    onSelect(val);
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <p className="text-gray-600 mb-4">Select an amount to tip</p>
        
        {/* Preset Grid */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          {PRESETS.map((amt) => (
            <button
              key={amt}
              onClick={() => onSelect(amt)}
              className="py-3 px-4 rounded-xl border-2 border-gray-100 hover:border-zed-green hover:bg-zed-green/5 font-bold text-gray-700 transition-all"
            >
              K{amt}
            </button>
          ))}
        </div>
      </div>

      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <div className="w-full border-t border-gray-200"></div>
        </div>
        <div className="relative flex justify-center text-sm">
          <span className="px-2 bg-white text-gray-500">Or enter custom amount</span>
        </div>
      </div>

      {/* Custom Input */}
      <form onSubmit={handleCustomSubmit} className="relative">
        <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 font-bold">K</span>
        <input
          type="number"
          value={customAmount}
          onChange={(e) => {
            setCustomAmount(e.target.value);
            setError('');
          }}
          placeholder="0.00"
          className="w-full pl-8 pr-4 py-3 text-black bg-gray-50 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-zed-green text-lg font-bold"
        />
        {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        
        <button 
          type="submit"
          disabled={!customAmount}
          className="w-full mt-4 bg-zed-black text-white py-3.5 rounded-xl font-bold disabled:opacity-50 hover:bg-gray-800 transition-colors"
        >
          Continue
        </button>
      </form>
    </div>
  );
}

export default AmountSelector;