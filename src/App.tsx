import React, { useRef, useState } from 'react';
import { useReactToPrint } from 'react-to-print';
import { Printer, Sparkles } from 'lucide-react';

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

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8 no-print">
          <h1 className="text-3xl font-bold text-sky-700">Planificador Semanal de Menús</h1>
          <div className="flex gap-3">
            <button
              onClick={() => setShowAIModal(true)}
              className="flex items-center gap-2 bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              <Sparkles size={20} />
              Generar con IA
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
    </div>
  );
}

export default App;