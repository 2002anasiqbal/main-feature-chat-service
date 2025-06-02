import { ProgressBar } from "./ProgressBar";

// ProfileStrengthPanel.jsx
export function ProfileStrengthPanel({ strength }) {
    return (
      <div className="border rounded-md p-4 mb-4">
        <h3 className="text-base font-medium mb-1">Profile strength({strength}%)</h3>
        <ProgressBar percentage={strength} />
        <p className="text-sm mt-3 mb-1">Fill in the telephone number for a more complete FINN Job profile.</p>
        <a href="#" className="text-teal-600 hover:text-teal-700 text-sm font-medium">Fill the number</a>
      </div>
    );
  }