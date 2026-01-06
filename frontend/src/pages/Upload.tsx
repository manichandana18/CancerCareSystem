import { useState } from "react";

export default function Upload() {
  const [image, setImage] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleAnalyze = () => {
    if (!image) {
      alert("Please upload an image first");
      return;
    }

    alert("Image ready to send to backend");
  };

  return (
    <section className="space-y-6 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold">Upload X-ray Image</h1>

      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
      />

      {image && (
        <p className="text-sm text-gray-600">
          Selected: {image.name}
        </p>
      )}

      {preview && (
        <img
          src={preview}
          alt="X-ray preview"
          className="max-h-96 rounded border"
        />
      )}

      <button
        onClick={handleAnalyze}
        className="px-6 py-3 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Analyze Image
      </button>
    </section>
  );
}
