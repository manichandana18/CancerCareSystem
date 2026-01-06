import Navbar from "../Navbar";
import { ReactNode } from "react";

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <>
      <Navbar />
      <main style={{ padding: "24px" }}>
        {children}
      </main>
    </>
  );
}
