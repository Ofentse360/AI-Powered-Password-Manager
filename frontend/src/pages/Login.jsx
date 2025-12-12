import { Link } from "react-router-dom";

export default function Login() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white">
      <div className="p-8 bg-gray-800 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold mb-4">Login</h1>
        <p>Form goes here...</p>
        <Link to="/register" className="text-blue-400 hover:underline mt-4 block">
          Need an account? Register
        </Link>
      </div>
    </div>
  );
}