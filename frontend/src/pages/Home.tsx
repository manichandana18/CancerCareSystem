import { Link } from "react-router-dom";

export default function Home() {
  return (
    <section className="space-y-24">

      {/* Hero */}
      <div className="text-center max-w-4xl mx-auto">
        <h1 className="text-5xl font-extrabold text-gray-900">
          Bone X-ray Analysis
        </h1>

        <p className="mt-6 text-lg text-gray-600">
          Upload a bone X-ray image to receive a structured screening result.
          Designed for educational and analytical purposes.
        </p>

        <div className="mt-10 flex justify-center gap-4">
          <Link to="/upload">
            <button className="px-6 py-3 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition">
              Upload X-ray
            </button>
          </Link>

          <Link to="/learn">
            <button className="px-6 py-3 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-100 transition">
              Learn More
            </button>
          </Link>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="p-6 rounded-xl border bg-white shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800">
            Image-Based Screening
          </h3>
          <p className="mt-2 text-sm text-gray-600">
            Processes uploaded X-ray images to identify visual patterns.
          </p>
        </div>

        <div className="p-6 rounded-xl border bg-white shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800">
            Confidence Indicators
          </h3>
          <p className="mt-2 text-sm text-gray-600">
            Provides a confidence score to help interpret the result.
          </p>
        </div>

        <div className="p-6 rounded-xl border bg-white shadow-sm">
          <h3 className="text-lg font-semibold text-gray-800">
            Educational Use
          </h3>
          <p className="mt-2 text-sm text-gray-600">
            Intended for learning and demonstration, not medical diagnosis.
          </p>
        </div>
      </div>

      {/* Disclaimer */}
      <p className="text-center text-sm text-gray-500">
        This tool is for educational purposes only and does not replace
        professional medical advice.
      </p>

    </section>
  );
}
