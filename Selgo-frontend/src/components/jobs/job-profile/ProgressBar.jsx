// ProgressBar.jsx
export function ProgressBar({ percentage, height = 8 }) {
    return (
      <div className="w-full bg-gray-200 rounded-full" style={{ height: `${height}px` }}>
        <div 
          className="bg-teal-600 rounded-full" 
          style={{ width: `${percentage}%`, height: '100%' }}
        ></div>
      </div>
    );
  }