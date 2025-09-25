// src/app/layout.tsx
import './globals.css';
import type { ReactNode } from 'react';
import AuthProvider from './AuthProvider';

export const metadata = {
  title: 'AI Risk Guardian',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es">
      <body className="flex h-screen bg-gray-50 antialiased">
        <AuthProvider>
          <aside className="w-64 bg-gradient-to-b from-green-900 to-green-800 text-white p-6 shadow-xl">
            <div className="flex items-center gap-3 mb-8">
              <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-600 rounded-lg flex items-center justify-center">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5-6v6a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold">AI Risk Guardian</h1>
                <p className="text-gray-400 text-sm">Model Risk Management</p>
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="text-green-300 text-sm font-medium mb-4">Acerca del Proyecto</div>
              <div className="text-green-100 text-sm leading-relaxed space-y-3">
                <p>
                  <strong className="text-white">AI Risk Guardian</strong> es un asistente inteligente especializado en Model Risk Management para instituciones financieras.
                </p>
                <p>
                  Proporciona orientación experta sobre validación de modelos, cumplimiento regulatorio, gestión de riesgos y documentación técnica.
                </p>
                <p>
                  Diseñado específicamente para profesionales del sector bancario que trabajan con modelos de riesgo y necesitan consultas especializadas.
                </p>
              </div>
            </div>
          </aside>
          <main className="flex-1 overflow-auto bg-white">
            {children}
          </main>
        </AuthProvider>
      </body>
    </html>
  );
}
