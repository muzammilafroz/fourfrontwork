import { Link } from "react-router-dom";
import SwaggerUI from "swagger-ui-react";
import "swagger-ui-react/swagger-ui.css";

import { Button } from "@/components/ui/button";

const ApiDocs = () => {
  return (
    <div className="min-h-screen bg-background p-4 md:p-6">
      <div className="mx-auto max-w-7xl">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold text-foreground">API Documentation</h1>
            <p className="text-sm text-muted-foreground">
              Interactive OpenAPI Swagger UI rendered inside the app.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button asChild variant="outline">
              <a href="/openapi.yaml" target="_blank" rel="noreferrer">
                OpenAPI YAML
              </a>
            </Button>
            <Button asChild variant="outline">
              <a href="/redoc" target="_blank" rel="noreferrer">
                ReDoc
              </a>
            </Button>
            <Button asChild>
              <Link to="/">Back to Home</Link>
            </Button>
          </div>
        </div>

        <div className="overflow-hidden rounded-lg border border-border bg-card">
          <SwaggerUI url="/openapi.yaml" docExpansion="list" defaultModelsExpandDepth={-1} />
        </div>
      </div>
    </div>
  );
};

export default ApiDocs;