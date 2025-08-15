export function ResumePanel() {
    return (
      <div className="border rounded-md p-4">
        <h3 className="text-base font-medium mb-2">Resume</h3>
        <p className="text-sm mb-2">Create a CV with the content from your Job Profile.</p>
        <a href="#" className="text-teal-600 hover:text-teal-700 text-sm font-medium block mb-4">Download job profile as cv</a>
        <p className="text-sm mb-2">or upload your own CV so that it is easily accessible when you are looking for jobs.</p>
        <a href="#" className="text-teal-600 hover:text-teal-700 text-sm font-medium">Add cv</a>
      </div>
    );
  }