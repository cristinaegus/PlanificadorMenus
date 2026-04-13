import React, { useRef, useState } from 'react';
import { useReactToPrint } from 'react-to-print';
import { Printer, Sparkles, List, UtensilsCrossed, Heart, FileText, Download, Info } from 'lucide-react';
import RecipeList from './RecipeList';
import MenuSelector from './MenuSelector';

type Meal = {
  breakfast: string;
  lunch: string;
  dinner: string;
};

type WeeklyPlan = {
  [key: string]: Meal;
};

type PrintableContentProps = {
  weeklyPlan: WeeklyPlan;
  weekDays: string[];
  handleMealChange: (day: string, meal: keyof Meal, value: string) => void;
};

type PrintableContentWithNameProps = PrintableContentProps & { nombre: string };

const PrintableContent = React.forwardRef<HTMLDivElement, PrintableContentWithNameProps>(
  ({ weeklyPlan, weekDays, handleMealChange, nombre }, ref) => (
    <div ref={ref} className="bg-white p-8 rounded-xl shadow-lg overflow-x-auto">
      <table className="w-full border border-gray-400 border-collapse">
        <thead>
          <tr>
            <th className="border p-3 bg-gray-50 text-center align-middle min-w-[80px]">{nombre}</th>
            {weekDays.map((day) => (
              <th key={day} className="border p-3 bg-gray-50 text-center">{day}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {/* Fila Comida */}
          <tr>
            <td className="border p-3 font-medium bg-gray-50 text-center align-middle min-w-[80px]">{nombre}</td>
            {weekDays.map((day) => (
              <td key={day} className="border p-2">
                <textarea
                  className="w-full p-2 min-h-[60px] border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={typeof weeklyPlan[day]?.lunch === 'string' ? weeklyPlan[day].lunch : ''}
                  onChange={(e) => handleMealChange(day, 'lunch', e.target.value)}
                  placeholder="Añadir comida..."
                />
              </td>
            ))}
          </tr>
          {/* Fila Cena */}
          <tr>
            <td className="border p-3 bg-gray-50"></td>
            {weekDays.map((day) => (
              <td key={day} className="border p-2">
                <textarea
                  className="w-full p-2 min-h-[60px] border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={typeof weeklyPlan[day]?.dinner === 'string' ? weeklyPlan[day].dinner : ''}
                  onChange={(e) => handleMealChange(day, 'dinner', e.target.value)}
                  placeholder="Añadir cena..."
                />
              </td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  )
);

PrintableContent.displayName = 'PrintableContent';

function App() {
  const componentRef = useRef<HTMLDivElement>(null);
  const weekDays = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];

  // Estado de navegación
  const [currentView, setCurrentView] = useState<'planner' | 'recipes' | 'menu'>('planner');

  // Estado independiente para Cristina y Marisa
  const [weeklyPlanCristina, setWeeklyPlanCristina] = React.useState<WeeklyPlan>(() => {
    const initialPlan: WeeklyPlan = {};
    weekDays.forEach(day => {
      initialPlan[day] = { breakfast: '', lunch: '', dinner: '' };
    });
    return initialPlan;
  });
  const [weeklyPlanMarisa, setWeeklyPlanMarisa] = React.useState<WeeklyPlan>(() => {
    const initialPlan: WeeklyPlan = {};
    weekDays.forEach(day => {
      initialPlan[day] = { breakfast: '', lunch: '', dinner: '' };
    });
    return initialPlan;
  });

  // Estados para la generación con IA
  const [showAIModal, setShowAIModal] = useState(false);
  const [selectedPerson, setSelectedPerson] = useState<'Cristina' | 'Marisa'>('Cristina');
  const [aiPreferences, setAiPreferences] = useState('');
  const [aiRestrictions, setAiRestrictions] = useState('');
  const [aiCuisineType, setAiCuisineType] = useState('mediterránea');
  const [isGenerating, setIsGenerating] = useState(false);

  // Estados para las dietas médicas
  const [showMedicalDietsModal, setShowMedicalDietsModal] = useState(false);
  const [downloadingDiet, setDownloadingDiet] = useState<number | null>(null);

  const handlePrint = useReactToPrint({
    content: () => componentRef.current,
    documentTitle: 'Planificador Semanal de Menús',
    pageStyle: `@media print {
      @page { size: landscape; margin: 1cm; }
      body { background: white !important; }
      .print-container { display: flex; flex-direction: row; gap: 2rem; align-items: flex-start; }
      .print-table { width: 100%; max-width: 100%; box-shadow: none !important; }
      .print-title { text-align: center; font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem; }
      .no-print { display: none !important; }
    }`
  });

  const handleMealChangeCristina = (day: string, meal: keyof Meal, value: string) => {
    setWeeklyPlanCristina(prev => ({
      ...prev,
      [day]: {
        ...prev[day],
        [meal]: value
      }
    }));
  };
  const handleMealChangeMarisa = (day: string, meal: keyof Meal, value: string) => {
    setWeeklyPlanMarisa(prev => ({
      ...prev,
      [day]: {
        ...prev[day],
        [meal]: value
      }
    }));
  };

  // Función para generar menú con IA
  const generateMenuWithAI = async () => {
    setIsGenerating(true);
    try {
      const response = await fetch('http://localhost:8000/generar-menu', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          preferencias: aiPreferences,
          restricciones: aiRestrictions,
          tipo_cocina: aiCuisineType,
        }),
      });

      if (!response.ok) {
        throw new Error('Error al generar el menú');
      }

      const data = await response.json();
      
      // Aplicar el menú generado a la persona seleccionada
      const generatedMenu: WeeklyPlan = {};
      weekDays.forEach(day => {
        generatedMenu[day] = {
          breakfast: '',
          lunch: data.menu[day]?.lunch || '',
          dinner: data.menu[day]?.dinner || '',
        };
      });

      if (selectedPerson === 'Cristina') {
        setWeeklyPlanCristina(generatedMenu);
      } else {
        setWeeklyPlanMarisa(generatedMenu);
      }

      setShowAIModal(false);
      alert('¡Menú generado con éxito!');
    } catch (error) {
      console.error('Error:', error);
      alert('Error al generar el menú. Asegúrate de que el backend esté funcionando en http://localhost:8000');
    } finally {
      setIsGenerating(false);
    }
  };

  // Función para generar y descargar menú de casa
  const handleMenuCasa = async () => {
    try {
      const response = await fetch('http://localhost:8000/generar-menu-casa', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id_cristina: 1,
          id_marisa: 1
        }),
      });

      if (!response.ok) {
        throw new Error('Error al generar el menú de casa');
      }

      // Convertir la respuesta a blob (archivo)
      const blob = await response.blob();
      
      // Crear un enlace temporal para descargar el archivo
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'menu_semanal_casa.pdf';
      document.body.appendChild(link);
      link.click();
      
      // Limpiar
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
      
      alert('¡PDF del Menú Casa descargado con éxito!');
    } catch (error) {
      console.error('Error:', error);
      alert('Error al generar el menú de casa. Asegúrate de que el backend esté funcionando.');
    }
  };

  // Funciones para dietas médicas
  const downloadMedicalDiet = async (modelNumber: number | 'complete' | 'summary') => {
    try {
      if (typeof modelNumber === 'number') {
        setDownloadingDiet(modelNumber);
      }

      let url = '';
      let filename = '';

      if (modelNumber === 'complete') {
        url = 'http://localhost:8001/dieta-modelos/generar-pdf-completo';
        filename = 'modelos_dieta_completos.pdf';
      } else if (modelNumber === 'summary') {
        url = 'http://localhost:8001/dieta-modelos/generar-resumen';
        filename = 'resumen_modelos_dieta.pdf';
      } else {
        url = `http://localhost:8001/dieta-modelos/generar-pdf-modelo/${modelNumber}`;
        filename = `modelo_dieta_${modelNumber}.pdf`;
      }

      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`Error al descargar: ${response.statusText}`);
      }

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
      
      alert(`¡PDF ${filename} descargado con éxito!`);
    } catch (error) {
      console.error('Error:', error);
      alert('Error al descargar el PDF. Asegúrate de que el backend esté funcionando en el puerto 8001.');
    } finally {
      setDownloadingDiet(null);
    }
  };

  const viewDietInfo = async () => {
    try {
      const response = await fetch('http://localhost:8001/dieta-modelos/info');
      if (!response.ok) {
        throw new Error('Error al obtener información');
      }
      const data = await response.json();
      
      // Mostrar información en una ventana nueva o modal
      const infoWindow = window.open('', '_blank', 'width=800,height=600');
      infoWindow?.document.write(`
        <html>
          <head>
            <title>Información de Modelos de Dieta</title>
            <style>
              body { font-family: Arial, sans-serif; padding: 20px; line-height: 1.6; }
              h1 { color: #2c3e50; }
              .model { margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; }
              .description { color: #7f8c8d; margin-bottom: 10px; }
            </style>
          </head>
          <body>
            <h1>📋 Modelos de Dieta OSAKIDETZA</h1>
            <div class="description">
              <p><strong>Descripción:</strong> ${data.descripcion}</p>
              <p><strong>Modelos disponibles:</strong> ${data.modelos_disponibles.join(', ')}</p>
            </div>
            <pre style="background: #f4f4f4; padding: 15px; border-radius: 5px; overflow: auto;">
${JSON.stringify(data.modelos, null, 2)}
            </pre>
          </body>
        </html>
      `);
    } catch (error) {
      console.error('Error:', error);
      alert('Error al obtener información. Asegúrate de que el backend esté funcionando.');
    }
  };

  // Mostrar vista de listado de recetas
  if (currentView === 'recipes') {
    return <RecipeList onBack={() => setCurrentView('planner')} />;
  }

  // Mostrar vista de selector de menú
  if (currentView === 'menu') {
    return <MenuSelector onBack={() => setCurrentView('planner')} />;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8 no-print">
          <h1 className="text-3xl font-bold text-sky-700">Planificador Semanal de Menús</h1>
          <div className="flex gap-3">
            <button
              onClick={() => setCurrentView('menu')}
              className="flex items-center gap-2 bg-orange-600 text-white px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors"
            >
              <UtensilsCrossed size={20} />
              Elige Menú
            </button>
            <button
              onClick={() => setCurrentView('recipes')}
              className="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              <List size={20} />
              Listado de Platos
            </button>
            <button
              onClick={() => handleMenuCasa()}
              className="flex items-center gap-2 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
            >
              <UtensilsCrossed size={20} />
              Menú Casa
            </button>
            <button
              onClick={() => setShowAIModal(true)}
              className="flex items-center gap-2 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              <Sparkles size={20} />
              Generar con IA
            </button>
            <button
              onClick={() => setShowMedicalDietsModal(true)}
              className="flex items-center gap-2 bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 transition-colors"
            >
              <Heart size={20} />
              Dietas Médicas
            </button>
            <button
              onClick={handlePrint}
              className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Printer size={20} />
              Imprimir PDF
            </button>
          </div>
        </div>
        {/* Contenedor para impresión horizontal */}
        <div ref={componentRef} className="print-container flex flex-col gap-8">
          {/* Tabla Cristina */}
          <div className="mb-12 print-table w-full overflow-x-auto">
            <PrintableContent
              weeklyPlan={weeklyPlanCristina}
              weekDays={weekDays}
              handleMealChange={handleMealChangeCristina}
              nombre="Cristina"
            />
          </div>
          {/* Tabla Marisa */}
          <div className="print-table w-full overflow-x-auto">
            <PrintableContent
              weeklyPlan={weeklyPlanMarisa}
              weekDays={weekDays}
              handleMealChange={handleMealChangeMarisa}
              nombre="Marisa"
            />
          </div>
        </div>
      </div>

      {/* Modal para generar menú con IA */}
      {showAIModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 no-print">
          <div className="bg-white rounded-xl shadow-2xl p-8 max-w-md w-full mx-4">
            <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
              <Sparkles className="text-purple-600" size={28} />
              Generar Menú con IA
            </h2>
          
          <div className="space-y-4">
            {/* Selector de persona */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Generar menú para:
              </label>
              <div className="flex gap-2">
                <button
                  onClick={() => setSelectedPerson('Cristina')}
                  className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                    selectedPerson === 'Cristina'
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  Cristina
                </button>
                <button
                  onClick={() => setSelectedPerson('Marisa')}
                  className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                    selectedPerson === 'Marisa'
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  Marisa
                </button>
              </div>
            </div>

            {/* Tipo de cocina */}
            <div>
              <label htmlFor="cuisine-type" className="block text-sm font-medium text-gray-700 mb-2">
                Tipo de cocina:
              </label>
              <select
                id="cuisine-type"
                value={aiCuisineType}
                onChange={(e) => setAiCuisineType(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="mediterránea">Mediterránea</option>
                <option value="asiática">Asiática</option>
                <option value="mexicana">Mexicana</option>
                <option value="italiana">Italiana</option>
                <option value="española">Española</option>
                <option value="vegetariana">Vegetariana</option>
                <option value="saludable">Saludable</option>
              </select>
            </div>

            {/* Preferencias */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Preferencias (opcional):
              </label>
              <input
                type="text"
                value={aiPreferences}
                onChange={(e) => setAiPreferences(e.target.value)}
                placeholder="Ej: Me gusta el pescado y las verduras"
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            {/* Restricciones */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Restricciones (opcional):
              </label>
              <input
                type="text"
                value={aiRestrictions}
                onChange={(e) => setAiRestrictions(e.target.value)}
                placeholder="Ej: Sin gluten, sin lácteos"
                className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
            </div>

            {/* Botones */}
            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowAIModal(false)}
                disabled={isGenerating}
                className="flex-1 py-2 px-4 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors disabled:opacity-50"
              >
                Cancelar
              </button>
              <button
                onClick={generateMenuWithAI}
                disabled={isGenerating}
                className="flex-1 py-2 px-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {isGenerating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Generando...
                  </>
                ) : (
                  <>
                    <Sparkles size={18} />
                    Generar
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
      )}

      {/* Modal para Dietas Médicas */}
      {showMedicalDietsModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 no-print">
          <div className="bg-white rounded-xl shadow-2xl p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                <Heart className="text-teal-600" size={28} />
                Dietas Médicas OSAKIDETZA
              </h2>
              <button
                onClick={() => setShowMedicalDietsModal(false)}
                className="text-gray-500 hover:text-gray-700 text-xl font-bold"
              >
                ×
              </button>
            </div>
            
            <div className="space-y-6">
              {/* Descripción */}
              <div className="bg-teal-50 border-l-4 border-teal-500 p-4 rounded-r-lg">
                <p className="text-teal-800 font-medium">
                  📋 Modelos de dieta de 1000 kcal para cirugía de obesidad
                </p>
                <p className="text-teal-600 text-sm mt-1">
                  Unidad de Nutrición 2015 - 4 modelos disponibles
                </p>
              </div>

              {/* Botones de descarga principal */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button
                  onClick={() => downloadMedicalDiet('complete')}
                  disabled={downloadingDiet !== null}
                  className="flex items-center gap-3 p-4 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors disabled:opacity-50"
                >
                  <FileText size={24} />
                  <div className="text-left">
                    <div className="font-semibold">PDF Completo</div>
                    <div className="text-sm opacity-90">Todos los 4 modelos</div>
                  </div>
                </button>

                <button
                  onClick={() => downloadMedicalDiet('summary')}
                  disabled={downloadingDiet !== null}
                  className="flex items-center gap-3 p-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  <FileText size={24} />
                  <div className="text-left">
                    <div className="font-semibold">Tabla Resumen</div>
                    <div className="text-sm opacity-90">Vista comparativa</div>
                  </div>
                </button>
              </div>

              {/* Modelos individuales */}
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Modelos Individuales:</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {[1, 2, 3, 4].map((modelNumber) => (
                    <button
                      key={modelNumber}
                      onClick={() => downloadMedicalDiet(modelNumber)}
                      disabled={downloadingDiet === modelNumber}
                      className="flex flex-col items-center gap-2 p-4 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {downloadingDiet === modelNumber ? (
                        <>
                          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white"></div>
                          <span className="text-sm">Descargando...</span>
                        </>
                      ) : (
                        <>
                          <Download size={20} />
                          <span className="font-medium">Modelo {modelNumber}</span>
                        </>
                      )}
                    </button>
                  ))}
                </div>
              </div>

              {/* Información adicional */}
              <div className="border-t pt-4">
                <button
                  onClick={viewDietInfo}
                  className="flex items-center gap-2 text-teal-600 hover:text-teal-800 transition-colors"
                >
                  <Info size={18} />
                  Ver información detallada (JSON)
                </button>
              </div>

              {/* Botón cerrar */}
              <div className="flex justify-end pt-4 border-t">
                <button
                  onClick={() => setShowMedicalDietsModal(false)}
                  className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
                >
                  Cerrar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;