import React, { useState, useRef } from 'react';
import { ChevronLeft, Plus, Trash2, Download } from 'lucide-react';
import { useReactToPrint } from 'react-to-print';

type MenuOption = {
  id: number;
  name: string;
  options: string[];
  selectedOption: string;
};

type MenuSelectorProps = {
  onBack: () => void;
};

const MenuSelector: React.FC<MenuSelectorProps> = ({ onBack }) => {
  const printRef = useRef<HTMLDivElement>(null);
  
  // Estado inicial con algunas opciones de menú predefinidas
  const [menuSections, setMenuSections] = useState<MenuOption[]>([
    {
      id: 1,
      name: 'Entrante',
      options: [
        'Seleccionar...',
        'Ensalada mixta',
        'Ensalada César',
        'Gazpacho',
        'Crema de verduras',
        'Jamón ibérico',
        'Croquetas caseras'
      ],
      selectedOption: 'Seleccionar...'
    },
    {
      id: 2,
      name: 'Primer Plato',
      options: [
        'Seleccionar...',
        'Pasta carbonara',
        'Paella valenciana',
        'Arroz con verduras',
        'Lentejas estofadas',
        'Sopa de fideos',
        'Risotto de champiñones'
      ],
      selectedOption: 'Seleccionar...'
    },
    {
      id: 3,
      name: 'Segundo Plato',
      options: [
        'Seleccionar...',
        'Pollo al horno',
        'Pescado a la plancha',
        'Solomillo de ternera',
        'Merluza en salsa verde',
        'Pechuga de pavo',
        'Salmón al limón'
      ],
      selectedOption: 'Seleccionar...'
    },
    {
      id: 4,
      name: 'Postre',
      options: [
        'Seleccionar...',
        'Fruta de temporada',
        'Yogur natural',
        'Flan casero',
        'Tarta de queso',
        'Helado',
        'Macedonia de frutas'
      ],
      selectedOption: 'Seleccionar...'
    },
    {
      id: 5,
      name: 'Bebida',
      options: [
        'Seleccionar...',
        'Agua',
        'Vino tinto',
        'Vino blanco',
        'Cerveza',
        'Refresco',
        'Zumo natural'
      ],
      selectedOption: 'Seleccionar...'
    }
  ]);

  const [newSection, setNewSection] = useState({
    name: '',
    options: ''
  });

  const [showAddForm, setShowAddForm] = useState(false);

  // Actualizar opción seleccionada
  const handleOptionChange = (id: number, value: string) => {
    setMenuSections(prev =>
      prev.map(section =>
        section.id === id
          ? { ...section, selectedOption: value }
          : section
      )
    );
  };

  // Añadir nueva sección de menú
  const handleAddSection = () => {
    if (newSection.name.trim() && newSection.options.trim()) {
      const optionsArray = newSection.options
        .split(',')
        .map(opt => opt.trim())
        .filter(opt => opt.length > 0);

      const newMenuSection: MenuOption = {
        id: Date.now(),
        name: newSection.name,
        options: ['Seleccionar...', ...optionsArray],
        selectedOption: 'Seleccionar...'
      };

      setMenuSections([...menuSections, newMenuSection]);
      setNewSection({ name: '', options: '' });
      setShowAddForm(false);
    }
  };

  // Eliminar sección
  const handleDeleteSection = (id: number) => {
    setMenuSections(menuSections.filter(section => section.id !== id));
  };

  // Resetear todas las selecciones
  const handleReset = () => {
    setMenuSections(prev =>
      prev.map(section => ({
        ...section,
        selectedOption: 'Seleccionar...'
      }))
    );
  };

  // Configurar impresión
  const handlePrint = useReactToPrint({
    content: () => printRef.current,
    documentTitle: 'Menú Seleccionado',
    pageStyle: `
      @media print {
        @page { 
          size: A4 portrait; 
          margin: 2cm; 
        }
        body { 
          background: white !important; 
        }
        .no-print { 
          display: none !important; 
        }
      }
    `
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-yellow-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8 no-print">
          <button
            onClick={onBack}
            className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors mb-4"
          >
            <ChevronLeft className="w-5 h-5" />
            Volver al Planificador
          </button>
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🍽️ Elige tu Menú
          </h1>
          <p className="text-gray-600">Selecciona las opciones para cada categoría del menú</p>
        </div>

        {/* Botones de acción */}
        <div className="flex gap-3 mb-6 no-print">
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow-md"
          >
            <Plus className="w-5 h-5" />
            Añadir Categoría
          </button>
          <button
            onClick={handleReset}
            className="flex items-center gap-2 px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors shadow-md"
          >
            Resetear Selección
          </button>
          <button
            onClick={handlePrint}
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors shadow-md ml-auto"
          >
            <Download className="w-5 h-5" />
            Descargar PDF
          </button>
        </div>

        {/* Formulario para añadir nueva categoría */}
        {showAddForm && (
          <div className="bg-white rounded-xl shadow-md p-6 mb-6 no-print">
            <h3 className="text-xl font-semibold mb-4">Nueva Categoría de Menú</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre de la Categoría *
                </label>
                <input
                  type="text"
                  value={newSection.name}
                  onChange={(e) => setNewSection({ ...newSection, name: e.target.value })}
                  placeholder="Ej: Guarnición"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Opciones (separadas por comas) *
                </label>
                <textarea
                  value={newSection.options}
                  onChange={(e) => setNewSection({ ...newSection, options: e.target.value })}
                  placeholder="Ej: Patatas fritas, Ensalada, Verduras al vapor"
                  rows={3}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={handleAddSection}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Guardar Categoría
              </button>
              <button
                onClick={() => {
                  setShowAddForm(false);
                  setNewSection({ name: '', options: '' });
                }}
                className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
              >
                Cancelar
              </button>
            </div>
          </div>
        )}

        {/* Contenido imprimible */}
        <div ref={printRef} className="bg-white rounded-xl shadow-lg p-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-800 mb-2">Menú del Día</h2>
            <p className="text-gray-600">{new Date().toLocaleDateString('es-ES', { 
              weekday: 'long', 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric' 
            })}</p>
          </div>

          {/* Listado de categorías con selectores */}
          <div className="space-y-6">
            {menuSections.map((section) => (
              <div key={section.id} className="border-b border-gray-200 pb-6 last:border-b-0">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-xl font-semibold text-gray-800">
                    {section.name}
                  </h3>
                  <button
                    onClick={() => handleDeleteSection(section.id)}
                    className="no-print p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Eliminar categoría"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>

                {/* Selector desplegable */}
                <select
                  value={section.selectedOption}
                  onChange={(e) => handleOptionChange(section.id, e.target.value)}
                  className="w-full px-4 py-3 text-lg border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all print:border-0 print:px-0 print:py-1"
                  aria-label={`Seleccionar ${section.name}`}
                >
                  {section.options.map((option, idx) => (
                    <option 
                      key={idx} 
                      value={option}
                      disabled={option === 'Seleccionar...'}
                    >
                      {option}
                    </option>
                  ))}
                </select>

                {/* Mostrar selección en formato de impresión */}
                {section.selectedOption !== 'Seleccionar...' && (
                  <div className="hidden print:block mt-2">
                    <p className="text-lg text-gray-700 font-medium">
                      → {section.selectedOption}
                    </p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Resumen (solo visible en impresión) */}
          <div className="hidden print:block mt-12 pt-6 border-t-2 border-gray-300">
            <h3 className="text-xl font-bold text-gray-800 mb-4">Menú Completo:</h3>
            <div className="space-y-2">
              {menuSections
                .filter(section => section.selectedOption !== 'Seleccionar...')
                .map((section) => (
                  <div key={section.id} className="flex justify-between items-center">
                    <span className="font-semibold text-gray-700">{section.name}:</span>
                    <span className="text-gray-800">{section.selectedOption}</span>
                  </div>
                ))}
            </div>
          </div>
        </div>

        {/* Información adicional */}
        <div className="mt-6 p-4 bg-blue-50 rounded-lg no-print">
          <p className="text-sm text-blue-800">
            💡 <strong>Tip:</strong> Selecciona todas las opciones que desees y haz clic en "Descargar PDF" 
            para generar un documento imprimible con tu menú personalizado.
          </p>
        </div>
      </div>
    </div>
  );
};

export default MenuSelector;
