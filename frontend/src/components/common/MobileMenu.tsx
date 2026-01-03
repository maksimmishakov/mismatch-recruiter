import { useState } from 'react'
import { Link } from 'react-router-dom'
import Button from './Button'

export default function MobileMenu() {
  const [isOpen, setIsOpen] = useState(false)

  const toggleMenu = () => setIsOpen(!isOpen)

  return (
    <>
      <button
        onClick={toggleMenu}
        className="md:hidden fixed top-4 left-4 p-2 bg-gray-900 text-white rounded z-50"
        aria-label="Toggle menu"
      >
        {isOpen ? '×' : '☰'}
      </button>

      {isOpen && (
        <div className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-40" onClick={toggleMenu} />
      )}

      <nav
        className={`md:hidden fixed left-0 top-0 h-full w-64 bg-gray-900 text-white transform transition-transform z-50 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="p-6 space-y-4">
          <h2 className="text-xl font-bold">MisMatch</h2>
          
          <Link to="/" className="block px-4 py-2 rounded hover:bg-gray-800" onClick={toggleMenu}>
            Dashboard
          </Link>
          <Link to="/candidates" className="block px-4 py-2 rounded hover:bg-gray-800" onClick={toggleMenu}>
            Candidates
          </Link>
          <Link to="/jobs" className="block px-4 py-2 rounded hover:bg-gray-800" onClick={toggleMenu}>
            Jobs
          </Link>
          <Link to="/matches" className="block px-4 py-2 rounded hover:bg-gray-800" onClick={toggleMenu}>
            Matches
          </Link>
          
          <hr className="border-gray-700" />
          
          <Button variant="secondary" fullWidth>
            Logout
          </Button>
        </div>
      </nav>
    </>
  )
}
