// ProfileHeader.jsx
export function ProfileHeader({ title, description }) {
    return (
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-800 mb-2">{title}</h1>
        {description && <p className="text-sm text-gray-600">{description}</p>}
      </div>
    );
  }
  