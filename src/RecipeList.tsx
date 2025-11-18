import React, { useState } from 'react';
import { ChevronLeft, Plus, Trash2, Search } from 'lucide-react';

type Recipe = {
  id: number;
  name: string;
  category: string;
  cuisine: string;
  ingredients?: string;
};

type RecipeListProps = {
  onBack: () => void;
};

const RecipeList: React.FC<RecipeListProps> = ({ onBack }) => {
  const [recipes, setRecipes] = useState<Recipe[]>([
    { id: 1, name: 'Ensalada Griega con Queso Feta', category: 'Comida', cuisine: 'Mediterránea', ingredients: 'Tomate, pepino, aceitunas, queso feta, cebolla' },
    { id: 2, name: 'Pasta con Tomate y Albahaca', category: 'Comida', cuisine: 'Italiana', ingredients: 'Pasta, tomate, albahaca, ajo, aceite de oliva' },
    { id: 3, name: 'Sopa de Verduras', category: 'Cena', cuisine: 'Mediterránea', ingredients: 'Zanahoria, calabacín, puerro, apio, caldo' },
    { id: 4, name: 'Paella Valenciana', category: 'Comida', cuisine: 'Española', ingredients: 'Arroz, pollo, conejo, judías verdes, pimentón' },
    { id: 5, name: 'Tacos de Pollo', category: 'Comida', cuisine: 'Mexicana', ingredients: 'Tortillas, pollo, aguacate, tomate, cilantro' },
  ]);

  const [newRecipe, setNewRecipe] = useState<Omit<Recipe, 'id'>>({
    name: '',
    category: 'Comida',
    cuisine: 'Mediterránea',
    ingredients: '',
  });

  const [showAddForm, setShowAddForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('Todas');
  const [filterCuisine, setFilterCuisine] = useState('Todas');

  const categories = ['Todas', 'Comida', 'Cena'];
  const cuisines = ['Todas', 'Mediterránea', 'Italiana', 'Asiática', 'Mexicana', 'Española'];

  const handleAddRecipe = () => {
    if (newRecipe.name.trim()) {
      const recipe: Recipe = {
        id: Date.now(),
        ...newRecipe,
      };
      setRecipes([...recipes, recipe]);
      setNewRecipe({ name: '', category: 'Comida', cuisine: 'Mediterránea', ingredients: '' });
      setShowAddForm(false);
    }
  };

  const handleDeleteRecipe = (id: number) => {
    setRecipes(recipes.filter((recipe) => recipe.id !== id));
  };

  const filteredRecipes = recipes.filter((recipe) => {
    const matchesSearch = recipe.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         recipe.ingredients?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = filterCategory === 'Todas' || recipe.category === filterCategory;
    const matchesCuisine = filterCuisine === 'Todas' || recipe.cuisine === filterCuisine;
    return matchesSearch && matchesCategory && matchesCuisine;
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={onBack}
            className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors mb-4"
          >
            <ChevronLeft className="w-5 h-5" />
            Volver al Planificador
          </button>
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            📋 Listado de Platos
          </h1>
          <p className="text-gray-600">Gestiona tu catálogo de recetas para planificar menús</p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Buscar platos o ingredientes..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Category Filter */}
            <select
              value={filterCategory}
              onChange={(e) => setFilterCategory(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              aria-label="Filtrar por categoría"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat === 'Todas' ? 'Todas las categorías' : cat}
                </option>
              ))}
            </select>

            {/* Cuisine Filter */}
            <select
              value={filterCuisine}
              onChange={(e) => setFilterCuisine(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              aria-label="Filtrar por tipo de cocina"
            >
              {cuisines.map((cuisine) => (
                <option key={cuisine} value={cuisine}>
                  {cuisine === 'Todas' ? 'Todas las cocinas' : cuisine}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Add Button */}
        <div className="mb-6">
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors shadow-md"
          >
            <Plus className="w-5 h-5" />
            Añadir Nuevo Plato
          </button>
        </div>

        {/* Add Form */}
        {showAddForm && (
          <div className="bg-white rounded-xl shadow-md p-6 mb-6">
            <h3 className="text-xl font-semibold mb-4">Nuevo Plato</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre del Plato *
                </label>
                <input
                  type="text"
                  value={newRecipe.name}
                  onChange={(e) => setNewRecipe({ ...newRecipe, name: e.target.value })}
                  placeholder="Ej: Paella Valenciana"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Categoría
                </label>
                <select
                  value={newRecipe.category}
                  onChange={(e) => setNewRecipe({ ...newRecipe, category: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  aria-label="Seleccionar categoría"
                >
                  <option value="Comida">Comida</option>
                  <option value="Cena">Cena</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Tipo de Cocina
                </label>
                <select
                  value={newRecipe.cuisine}
                  onChange={(e) => setNewRecipe({ ...newRecipe, cuisine: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  aria-label="Seleccionar tipo de cocina"
                >
                  {cuisines.slice(1).map((cuisine) => (
                    <option key={cuisine} value={cuisine}>
                      {cuisine}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ingredientes principales
                </label>
                <input
                  type="text"
                  value={newRecipe.ingredients}
                  onChange={(e) => setNewRecipe({ ...newRecipe, ingredients: e.target.value })}
                  placeholder="Ej: Arroz, pollo, verduras"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <div className="flex gap-3 mt-6">
              <button
                onClick={handleAddRecipe}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Guardar Plato
              </button>
              <button
                onClick={() => {
                  setShowAddForm(false);
                  setNewRecipe({ name: '', category: 'Comida', cuisine: 'Mediterránea', ingredients: '' });
                }}
                className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition-colors"
              >
                Cancelar
              </button>
            </div>
          </div>
        )}

        {/* Recipe List */}
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          <div className="px-6 py-4 bg-gray-50 border-b">
            <h3 className="text-lg font-semibold text-gray-800">
              Platos Disponibles ({filteredRecipes.length})
            </h3>
          </div>

          {filteredRecipes.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              <p>No se encontraron platos con los filtros aplicados.</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {filteredRecipes.map((recipe) => (
                <div
                  key={recipe.id}
                  className="p-6 hover:bg-gray-50 transition-colors flex items-start justify-between"
                >
                  <div className="flex-1">
                    <h4 className="text-lg font-semibold text-gray-800 mb-2">
                      {recipe.name}
                    </h4>
                    <div className="flex gap-4 text-sm text-gray-600 mb-2">
                      <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full">
                        {recipe.category}
                      </span>
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full">
                        {recipe.cuisine}
                      </span>
                    </div>
                    {recipe.ingredients && (
                      <p className="text-sm text-gray-500">
                        <strong>Ingredientes:</strong> {recipe.ingredients}
                      </p>
                    )}
                  </div>

                  <button
                    onClick={() => handleDeleteRecipe(recipe.id)}
                    className="ml-4 p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                    title="Eliminar plato"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecipeList;
