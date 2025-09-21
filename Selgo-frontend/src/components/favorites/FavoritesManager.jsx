"use client";
import { useState, useEffect, createContext, useContext } from 'react';
import useAuthStore from '@/store/store';

// Create Favorites Context
const FavoritesContext = createContext();

export const useFavorites = () => {
  const context = useContext(FavoritesContext);
  if (!context) {
    throw new Error('useFavorites must be used within a FavoritesProvider');
  }
  return context;
};

// Favorites Provider Component
export const FavoritesProvider = ({ children }) => {
  const [favorites, setFavorites] = useState({
    cars: [],
    properties: [],
    jobs: [],
    travel: [],
    electronics: [],
    boats: [],
    motorcycles: [],
    commercialVehicles: [],
    carAuctions: [],
    holidayRentals: []
  });
  const [loading, setLoading] = useState(false);
  const { isAuthenticated, user } = useAuthStore();

  // Load favorites from localStorage on mount
  useEffect(() => {
    if (isAuthenticated && user) {
      loadFavoritesFromStorage();
    }
  }, [isAuthenticated, user]);

  const loadFavoritesFromStorage = () => {
    try {
      const storedFavorites = localStorage.getItem(`favorites_${user?.id}`);
      if (storedFavorites) {
        setFavorites(JSON.parse(storedFavorites));
      }
    } catch (error) {
      console.error('Error loading favorites from storage:', error);
    }
  };

  const saveFavoritesToStorage = (newFavorites) => {
    try {
      localStorage.setItem(`favorites_${user?.id}`, JSON.stringify(newFavorites));
    } catch (error) {
      console.error('Error saving favorites to storage:', error);
    }
  };

  const addToFavorites = async (item, category) => {
    if (!isAuthenticated) {
      // Show login prompt or redirect
      return false;
    }

    setLoading(true);
    try {
      const newFavorites = {
        ...favorites,
        [category]: [...favorites[category].filter(fav => fav.id !== item.id), item]
      };
      
      setFavorites(newFavorites);
      saveFavoritesToStorage(newFavorites);
      
      // Here you would typically also sync with the backend
      // await syncFavoriteWithBackend(item, category, 'add');
      
      return true;
    } catch (error) {
      console.error('Error adding to favorites:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const removeFromFavorites = async (itemId, category) => {
    setLoading(true);
    try {
      const newFavorites = {
        ...favorites,
        [category]: favorites[category].filter(fav => fav.id !== itemId)
      };
      
      setFavorites(newFavorites);
      saveFavoritesToStorage(newFavorites);
      
      // Here you would typically also sync with the backend
      // await syncFavoriteWithBackend({ id: itemId }, category, 'remove');
      
      return true;
    } catch (error) {
      console.error('Error removing from favorites:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const isFavorite = (itemId, category) => {
    return favorites[category]?.some(fav => fav.id === itemId) || false;
  };

  const getFavoritesByCategory = (category) => {
    return favorites[category] || [];
  };

  const getAllFavorites = () => {
    return Object.entries(favorites).reduce((acc, [category, items]) => {
      return [...acc, ...items.map(item => ({ ...item, category }))];
    }, []);
  };

  const getFavoritesCount = (category = null) => {
    if (category) {
      return favorites[category]?.length || 0;
    }
    return Object.values(favorites).reduce((total, items) => total + items.length, 0);
  };

  const clearAllFavorites = async () => {
    setLoading(true);
    try {
      const emptyFavorites = {
        cars: [],
        properties: [],
        jobs: [],
        travel: [],
        electronics: [],
        boats: [],
        motorcycles: [],
        commercialVehicles: [],
        carAuctions: [],
        holidayRentals: []
      };
      
      setFavorites(emptyFavorites);
      saveFavoritesToStorage(emptyFavorites);
      
      return true;
    } catch (error) {
      console.error('Error clearing favorites:', error);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const value = {
    favorites,
    loading,
    addToFavorites,
    removeFromFavorites,
    isFavorite,
    getFavoritesByCategory,
    getAllFavorites,
    getFavoritesCount,
    clearAllFavorites
  };

  return (
    <FavoritesContext.Provider value={value}>
      {children}
    </FavoritesContext.Provider>
  );
};

// Favorite Button Component
export const FavoriteButton = ({ 
  item, 
  category, 
  size = 'md',
  showText = false,
  className = '' 
}) => {
  const { addToFavorites, removeFromFavorites, isFavorite, loading } = useFavorites();
  const [isToggling, setIsToggling] = useState(false);
  const favorite = isFavorite(item.id, category);

  const handleToggle = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    setIsToggling(true);
    try {
      if (favorite) {
        await removeFromFavorites(item.id, category);
      } else {
        await addToFavorites(item, category);
      }
    } finally {
      setIsToggling(false);
    }
  };

  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  };

  const buttonSizeClasses = {
    sm: 'p-1',
    md: 'p-2',
    lg: 'p-3'
  };

  return (
    <button
      onClick={handleToggle}
      disabled={loading || isToggling}
      className={`
        ${buttonSizeClasses[size]}
        ${favorite ? 'text-red-500 hover:text-red-600' : 'text-gray-400 hover:text-red-500'}
        transition-colors duration-200 disabled:opacity-50
        ${className}
      `}
      title={favorite ? 'Remove from favorites' : 'Add to favorites'}
    >
      {isToggling ? (
        <div className={`animate-spin rounded-full border-2 border-current border-t-transparent ${sizeClasses[size]}`} />
      ) : (
        <svg 
          className={sizeClasses[size]} 
          fill={favorite ? 'currentColor' : 'none'} 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={2} 
            d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" 
          />
        </svg>
      )}
      {showText && (
        <span className="ml-1 text-sm">
          {favorite ? 'Favorited' : 'Add to Favorites'}
        </span>
      )}
    </button>
  );
};

// Favorites List Component
export const FavoritesList = ({ category = null, onItemClick }) => {
  const { getFavoritesByCategory, getAllFavorites, removeFromFavorites } = useFavorites();
  
  const items = category ? getFavoritesByCategory(category) : getAllFavorites();

  if (items.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-400 mb-4">
          <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No favorites yet</h3>
        <p className="text-gray-600">Items you favorite will appear here.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {items.map((item) => (
        <div 
          key={`${item.category || category}-${item.id}`}
          className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
          onClick={() => onItemClick && onItemClick(item)}
        >
          {/* Image */}
          <div className="aspect-w-16 aspect-h-12 bg-gray-200">
            {item.images && item.images.length > 0 ? (
              <img
                src={item.images[0].image_url}
                alt={item.title}
                className="w-full h-48 object-cover"
              />
            ) : (
              <div className="w-full h-48 bg-gray-200 flex items-center justify-center">
                <span className="text-gray-400">No Image</span>
              </div>
            )}
          </div>

          {/* Content */}
          <div className="p-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-semibold text-lg text-gray-900 line-clamp-2 flex-1">
                {item.title}
              </h3>
              <FavoriteButton 
                item={item} 
                category={item.category || category}
                size="sm"
                className="ml-2 flex-shrink-0"
              />
            </div>
            
            <div className="flex items-center justify-between mb-2">
              <span className="text-2xl font-bold text-teal-600">
                ${item.price?.toLocaleString() || 'N/A'}
              </span>
              {item.category && (
                <span className="text-sm text-gray-500 capitalize bg-gray-100 px-2 py-1 rounded">
                  {item.category}
                </span>
              )}
            </div>

            <div className="text-sm text-gray-600">
              <p>{item.location}</p>
              <p className="text-xs text-gray-500 mt-1">
                Added {new Date(item.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

// Favorites Counter Component
export const FavoritesCounter = ({ category = null, className = '' }) => {
  const { getFavoritesCount } = useFavorites();
  const count = getFavoritesCount(category);

  if (count === 0) return null;

  return (
    <span className={`inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white bg-red-500 rounded-full ${className}`}>
      {count > 99 ? '99+' : count}
    </span>
  );
};

// Export the main provider as default
export default FavoritesProvider;