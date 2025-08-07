import React, { useRef } from 'react';
import { useReactToPrint } from 'react-to-print';
import { Printer } from 'lucide-react';

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

  const [weeklyPlan, setWeeklyPlan] = React.useState<WeeklyPlan>(() => {
    const initialPlan: WeeklyPlan = {};
    // Asegura que todos los días, incluido Domingo, estén presentes
    ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'].forEach(day => {
      initialPlan[day] = {
        breakfast: '',
        lunch: '',
        dinner: ''
      };
    });
    return initialPlan;
  });

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

  const handleMealChange = (day: string, meal: keyof Meal, value: string) => {
    setWeeklyPlan(prev => ({
      ...prev,
      [day]: {
        ...prev[day],
        [meal]: value
      }
    }));
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8 no-print">
          <h1 className="text-3xl font-bold text-sky-700">Planificador Semanal de Menús</h1>
          <button
            onClick={handlePrint}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Printer size={20} />
            Imprimir PDF
          </button>
        </div>
        {/* Contenedor para impresión horizontal */}
        <div ref={componentRef} className="print-container flex flex-col gap-8">
          {/* Tabla Cristina */}
          <div className="mb-12 print-table w-full overflow-x-auto">
            <PrintableContent
              weeklyPlan={weeklyPlan}
              weekDays={weekDays}
              handleMealChange={handleMealChange}
              nombre="Cristina"
            />
          </div>
          {/* Tabla Marisa */}
          <div className="print-table w-full overflow-x-auto">
            <PrintableContent
              weeklyPlan={weeklyPlan}
              weekDays={weekDays}
              handleMealChange={handleMealChange}
              nombre="Marisa"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;