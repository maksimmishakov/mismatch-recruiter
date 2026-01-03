import { Link } from 'react-router-dom';
export default function Sidebar() {
    return (<aside className="w-64 bg-gray-900 text-white flex flex-col">
      <div className="p-6 border-b border-gray-800">
        <h2 className="text-xl font-bold">MisMatch</h2>
        <p className="text-sm text-gray-400">AI Recruiter</p>
      </div>
      <nav className="flex-1 px-4 py-6 space-y-2">
        <Link to="/" className="block px-4 py-2 rounded hover:bg-gray-800 transition">
          🏢 Dashboard
        </Link>
        <Link to="/candidates" className="block px-4 py-2 rounded hover:bg-gray-800 transition">
          👥 Candidates
        </Link>
        <Link to="/jobs" className="block px-4 py-2 rounded hover:bg-gray-800 transition">
          💼 Jobs
        </Link>
        <Link to="/matches" className="block px-4 py-2 rounded hover:bg-gray-800 transition">
          ✨ Matches
        </Link>
      </nav>
      <div className="p-4 border-t border-gray-800">
        <button className="w-full px-4 py-2 bg-gray-800 rounded hover:bg-gray-700 transition">
          📤 Logout
        </button>
      </div>
    </aside>);
}
