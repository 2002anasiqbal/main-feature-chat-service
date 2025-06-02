// RecommendationsPanel.jsx
export function RecommendationsPanel({ email }) {
    return (
      <div className="border rounded-md p-4 mb-4">
        <h3 className="text-base font-medium mb-3">Recommendations</h3>
        <div className="flex mb-3">
          <div className="w-10 h-10 bg-teal-600 rounded-full mr-3 flex-shrink-0"></div>
          <p className="text-sm">Receive recommended jobs by email once a week.</p>
        </div>
        <p className="text-sm mb-2">The jobs will be sent by email to {email}</p>
        <a href="#" className="text-teal-600 hover:text-teal-700 text-sm font-medium">See recommended jobs</a>
      </div>
    );
  }