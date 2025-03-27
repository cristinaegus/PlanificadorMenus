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

const PrintableContent = React.forwardRef<HTMLDivElement, PrintableContentProps>(
  ({ weeklyPlan, weekDays, handleMealChange }, ref) => (
    <div ref={ref} className="bg-white p-8 rounded-xl shadow-lg">
      <table className="w-full border-collapse">
        <thead>
          <tr>
            <th className="border p-3 bg-gray-50">Día</th>
            <th className="border p-3 bg-gray-50">Desayuno</th>
            <th className="border p-3 bg-gray-50">Comida</th>
            <th className="border p-3 bg-gray-50">Cena</th>
          </tr>
        </thead>
        <tbody>
          {weekDays.map((day) => (
            <tr key={day}>
              <td className="border p-3 font-medium bg-gray-50">{day}</td>
              <td className="border p-2">
                <textarea
                  className="w-full p-2 min-h-[60px] border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={weeklyPlan[day].breakfast}
                  onChange={(e) => handleMealChange(day, 'breakfast', e.target.value)}
                  placeholder="Añadir desayuno..."
                />
              </td>
              <td className="border p-2">
                <textarea
                  className="w-full p-2 min-h-[60px] border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={weeklyPlan[day].lunch}
                  onChange={(e) => handleMealChange(day, 'lunch', e.target.value)}
                  placeholder="Añadir comida..."
                />
              </td>
              <td className="border p-2">
                <textarea
                  className="w-full p-2 min-h-[60px] border rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  value={weeklyPlan[day].dinner}
                  onChange={(e) => handleMealChange(day, 'dinner', e.target.value)}
                  placeholder="Añadir cena..."
                />
              </td>
            </tr>
          ))}
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
    weekDays.forEach(day => {
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
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-sky-700">Planificador Semanal de Menús</h1>
          <button
            onClick={handlePrint}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Printer size={20} />
            Imprimir PDF
          </button>
        </div>
        
        <PrintableContent
          ref={componentRef}
          weeklyPlan={weeklyPlan}
          weekDays={weekDays}
          handleMealChange={handleMealChange}
        />
      </div>
    </div>
  );
}

export default App;