import SavedSearches from "@/components/profile/SavedSearches";
const mockSearches = [
  { title: "Apartments in Oslo" },
  { title: "Electric Cars" },
  { title: "Remote Jobs" },
];
export default function SavedSearchesPage() {
  return (
    <div className="my-10">
      <SavedSearches searches={mockSearches} />;
    </div>
  );
}