import FindingsList from "@/components/profile/FindingLists";
const mockFindings = [
  { title: "My Findings", ads: 2 },
  { title: "Favorite Items", ads: 5 },
  { title: "Recently Viewed", ads: 3 },
];

export default function FavoritesPage() {
    return (
      <div className="my-10">
        <FindingsList findings={mockFindings}/>
      </div>
    );
  }