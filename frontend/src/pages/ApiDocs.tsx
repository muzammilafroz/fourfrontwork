import { Link } from "react-router-dom";
import { ArrowLeft, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";

const ApiDocs = () => {
  const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL as string | undefined) || "http://localhost:8000";
  const normalizedBase = apiBaseUrl.replace(/\/$/, "");
  const swaggerUrl = `${normalizedBase}/docs`;
  const openapiUrl = `${normalizedBase}/openapi.yaml`;

  return (
    <div className="min-h-screen bg-background">
      <div className="border-b border-border bg-card">
        <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-4 py-4 md:px-6">
          <div>
            <h1 className="text-2xl font-semibold text-foreground">API Docs</h1>
            <p className="text-sm text-muted-foreground">
              Swagger UI for all backend endpoints. Public endpoints are open; protected endpoints require JWT authorization.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Link to="/">
              <Button variant="outline" className="gap-2">
                <ArrowLeft className="h-4 w-4" />
                Back
              </Button>
            </Link>
            <a href={swaggerUrl} target="_blank" rel="noreferrer">
              <Button className="gap-2">
                Open in New Tab
                <ExternalLink className="h-4 w-4" />
              </Button>
            </a>
          </div>
        </div>
      </div>

      <div className="mx-auto w-full max-w-6xl px-4 py-4 md:px-6">
        <div className="mb-4 rounded-lg border border-border bg-card p-4 text-sm text-muted-foreground">
          <p>
            Endpoint index: <a className="text-primary underline" href={openapiUrl} target="_blank" rel="noreferrer">{openapiUrl}</a>
          </p>
        </div>

        <div className="overflow-hidden rounded-xl border border-border bg-card shadow-sm">
          <iframe
            title="Backend Swagger UI"
            src={swaggerUrl}
            className="h-[78vh] w-full"
          />
        </div>
      </div>
    </div>
  );
};

export default ApiDocs;