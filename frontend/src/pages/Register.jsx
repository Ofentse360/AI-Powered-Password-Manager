import { Link } from "react-router-dom";

export default function Register() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
      <div className="p-8 bg-gray-800 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold mb-4">Register</h1>
        <p>Registration form goes here...</p>
        <Link to="/login" className="text-blue-400 hover:underline mt-4 block">
          Already have an account? Login
        </Link>
      </div>
    </div>
  );
}