import { API_BASE_URL } from "../api/config";

export function HomePage() {
  return (
    <main>
      <h1>OddToBelieve</h1>
      <p>Betting odds aggregation dashboard</p>
      <p>
        <small>API: {API_BASE_URL}</small>
      </p>
    </main>
  );
}
