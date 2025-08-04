'use client';

import React, { useState, useEffect, useRef } from 'react';
import { ChevronDown, X, Tag } from 'lucide-react';
import { useBlogStore } from '@/store/blogStore';
import { Category } from '@/types';
import { cn } from '@/lib/utils';

interface CategoryFilterProps {
  className?: string;
  showAllOption?: boolean;
  placeholder?: string;
}

const CategoryFilter: React.FC<CategoryFilterProps> = ({
  className,
  showAllOption = true,
  placeholder = 'Filter by category',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const {
    categories,
    filters,
    setCategoryFilter,
    fetchCategories
  } = useBlogStore();

  // Fetch categories on mount
  useEffect(() => {
    if (categories.length === 0) {
      fetchCategories();
    }
  }, [categories.length, fetchCategories]);

  // Handle click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const selectedCategory = categories.find(cat => cat.id === filters.category);

  const handleCategorySelect = (categoryId: number | null) => {
    setCategoryFilter(categoryId);
    setIsOpen(false);
  };

  const handleClearFilter = () => {
    setCategoryFilter(null);
    setIsOpen(false);
  };

  return (
    <div className={cn('relative', className)}>
      <div className="relative">
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          className={cn(
            'w-full flex items-center justify-between px-3 py-2 border border-gray-300 rounded-lg bg-white text-left transition-all duration-200',
            isOpen && 'ring-2 ring-blue-500 border-transparent',
            selectedCategory && 'bg-blue-50 border-blue-200'
          )}
        >
          <div className="flex items-center gap-2 min-w-0 flex-1">
            <Tag className="w-4 h-4 text-gray-400 flex-shrink-0" />
            <span className={cn(
              'truncate',
              selectedCategory ? 'text-blue-700' : 'text-gray-500'
            )}>
              {selectedCategory ? selectedCategory.name : placeholder}
            </span>
          </div>

          <div className="flex items-center gap-1 flex-shrink-0">
            {selectedCategory && (
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  handleClearFilter();
                }}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
              >
                <X className="w-3 h-3 text-gray-400" />
              </button>
            )}
            <ChevronDown
              className={cn(
                'w-4 h-4 text-gray-400 transition-transform duration-200',
                isOpen && 'rotate-180'
              )}
            />
          </div>
        </button>
      </div>

      {/* Dropdown */}
      {isOpen && (
        <div
          ref={dropdownRef}
          className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto"
        >
          <div className="p-1">
            {showAllOption && (
              <button
                type="button"
                onClick={() => handleCategorySelect(null)}
                className={cn(
                  'w-full text-left px-3 py-2 text-sm rounded transition-colors',
                  !selectedCategory
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-700 hover:bg-gray-100'
                )}
              >
                All Categories
              </button>
            )}

            {categories.map((category) => (
              <button
                key={category.id}
                type="button"
                onClick={() => handleCategorySelect(category.id)}
                className={cn(
                  'w-full text-left px-3 py-2 text-sm rounded transition-colors',
                  selectedCategory?.id === category.id
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-700 hover:bg-gray-100'
                )}
              >
                <div className="flex items-center justify-between">
                  <span className="truncate">{category.name}</span>
                  <span className="text-xs text-gray-400 ml-2">
                    ({category.post_count})
                  </span>
                </div>
              </button>
            ))}

            {categories.length === 0 && (
              <div className="px-3 py-2 text-sm text-gray-500">
                No categories available
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CategoryFilter;
