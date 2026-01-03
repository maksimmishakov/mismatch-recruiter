export default function Header() {
    return (<header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">MisMatch Dashboard</h1>
        <div className="flex items-center gap-4">
          <button className="p-2 text-gray-600 hover:text-gray-900">
            🔔
          </button>
          <button className="p-2 text-gray-600 hover:text-gray-900">
            👤
          </button>
        </div>
      </div>
    </header>);
}
