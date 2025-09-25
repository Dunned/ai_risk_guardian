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
          <aside className="w-64 bg-gradient-to-b from-slate-800 to-slate-900 text-white p-6 shadow-xl border-r border-slate-700">
            <div className="flex items-center gap-3 mb-8">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center shadow-lg">
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
              <div className="text-blue-300 text-sm font-medium mb-4">Acerca del Proyecto</div>
              <div className="text-slate-300 text-sm leading-relaxed space-y-3">
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
          <main className="flex-1 overflow-auto bg-gradient-to-br from-slate-50 to-blue-50 relative">
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
              <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400/20 to-indigo-600/20 rounded-full blur-3xl animate-pulse"></div>
              <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-tr from-slate-400/20 to-blue-500/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
              <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-indigo-400/10 to-blue-600/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '4s'}}></div>
            </div>
            {children}
          </main>
        </AuthProvider>
      </body>
    </html>
  );
}
