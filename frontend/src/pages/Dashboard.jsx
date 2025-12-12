export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-4xl font-bold mb-6">My Vault</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gray-800 p-6 rounded-lg border border-gray-700">
          <h2 className="text-xl font-bold text-green-400">Strong Passwords</h2>
          <p className="text-4xl mt-2">12</p>
        </div>
        {/* More cards will go here */}
      </div>
    </div>
  );
}