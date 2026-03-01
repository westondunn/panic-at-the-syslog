/**
 * Sign In page – Material Dashboard–style auth form.
 * Uses AuthLayout (rendered via conditional in _app.js AUTH_ROUTES).
 */
import Link from "next/link";
import { useState } from "react";
import AuthLayout from "../components/AuthLayout";

export default function SignIn() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      // TODO: wire to real auth endpoint
      const res = await fetch("/api/v1/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || "Invalid credentials");
      }

      // Redirect to dashboard on success
      window.location.href = "/";
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout>
      {/* Gradient header inside card */}
      <div className="-mx-8 -mt-8 mb-6 rounded-t-card gradient-info px-8 py-8 text-center">
        <h1 className="text-2xl font-bold text-text-inverse">Sign In</h1>
        <p className="mt-1 text-sm text-text-inverse/70">
          Enter your credentials to continue
        </p>
      </div>

      {error && (
        <div className="mb-4 rounded-lg bg-error/10 px-4 py-2.5 text-sm text-error">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-5">
        <div>
          <label
            htmlFor="email"
            className="mb-1 block text-xs font-semibold uppercase tracking-wide text-text-secondary"
          >
            Email
          </label>
          <input
            id="email"
            type="email"
            required
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-lg border border-primary-100 bg-background px-4 py-2.5 text-sm text-text-primary placeholder:text-text-disabled outline-none transition focus:border-info focus:ring-2 focus:ring-info/20"
            placeholder="admin@panic.local"
          />
        </div>

        <div>
          <label
            htmlFor="password"
            className="mb-1 block text-xs font-semibold uppercase tracking-wide text-text-secondary"
          >
            Password
          </label>
          <input
            id="password"
            type="password"
            required
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-lg border border-primary-100 bg-background px-4 py-2.5 text-sm text-text-primary placeholder:text-text-disabled outline-none transition focus:border-info focus:ring-2 focus:ring-info/20"
            placeholder="••••••••"
          />
        </div>

        <label className="flex items-center gap-2 text-sm text-text-secondary">
          <input
            type="checkbox"
            checked={remember}
            onChange={(e) => setRemember(e.target.checked)}
            className="h-4 w-4 rounded border-primary-100 text-info focus:ring-info/20"
          />
          Remember me
        </label>

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg gradient-info py-2.5 text-sm font-semibold text-text-inverse shadow-stat transition-shadow hover:shadow-card-hover disabled:opacity-60"
        >
          {loading ? "Signing in…" : "Sign In"}
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-text-secondary">
        Don&apos;t have an account?{" "}
        <Link
          href="/sign-up"
          className="font-semibold text-info hover:underline"
        >
          Sign Up
        </Link>
      </p>
    </AuthLayout>
  );
}
