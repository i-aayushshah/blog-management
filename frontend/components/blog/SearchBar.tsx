'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Search, X, Loader2 } from 'lucide-react';
import { useBlogStore } from '@/store/blogStore';
import { debounce } from '@/lib/utils';
import { cn } from '@/lib/utils';

interface SearchBarProps {
  placeholder?: string;
  className?: string;
  onSearch?: (query: string) => void;
  showSuggestions?: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({
  placeholder = 'Search posts...',
  className,
  onSearch,
  showSuggestions = true,
}) => {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [showSuggestionsDropdown, setShowSuggestionsDropdown] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const { posts, setSearch, fetchPosts } = useBlogStore();

  // Debounced search function
  const debouncedSearch = useRef(
    debounce(async (searchQuery: string) => {
      if (searchQuery.trim()) {
        setIsSearching(true);
        try {
          await fetchPosts({ search: searchQuery });
        } catch (error) {
          console.error('Search error:', error);
        } finally {
          setIsSearching(false);
        }
      } else {
        // Clear search and fetch all posts
        await fetchPosts();
      }
    }, 300)
  ).current;

  // Handle search input change
  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setSearch(value);

    if (onSearch) {
      onSearch(value);
    } else {
      debouncedSearch(value);
    }
  };

  // Handle search submit
  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      debouncedSearch(query);
    }
  };

  // Clear search
  const handleClearSearch = () => {
    setQuery('');
    setSearch('');
    if (onSearch) {
      onSearch('');
    } else {
      fetchPosts();
    }
    inputRef.current?.focus();
  };

  // Handle click outside to close suggestions
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        inputRef.current &&
        !inputRef.current.contains(event.target as Node)
      ) {
        setShowSuggestionsDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Show suggestions when input is focused and has content
  const handleInputFocus = () => {
    if (query.trim() && showSuggestions) {
      setShowSuggestionsDropdown(true);
    }
  };

  // Generate search suggestions based on recent posts
  const getSearchSuggestions = () => {
    if (!posts || !Array.isArray(posts) || posts.length === 0) return [];

    const suggestions = new Set<string>();

    // Add titles
    posts.slice(0, 5).forEach(post => {
      if (post.title) {
        const words = post.title.toLowerCase().split(' ');
        words.forEach(word => {
          if (word.length > 2 && word.startsWith(query.toLowerCase())) {
            suggestions.add(word);
          }
        });
      }
    });

    // Add categories
    posts.forEach(post => {
      if (post.category?.name && post.category.name.toLowerCase().includes(query.toLowerCase())) {
        suggestions.add(post.category.name);
      }
    });

    // Add tags
    posts.forEach(post => {
      if (post.tags && Array.isArray(post.tags)) {
        post.tags.forEach(tag => {
          if (tag.name && tag.name.toLowerCase().includes(query.toLowerCase())) {
            suggestions.add(tag.name);
          }
        });
      }
    });

    return Array.from(suggestions).slice(0, 8);
  };

  const suggestions = getSearchSuggestions();

  return (
    <div className={cn('relative', className)}>
      <form onSubmit={handleSearchSubmit} className="relative">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />

          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={handleSearchChange}
            onFocus={handleInputFocus}
            placeholder={placeholder}
            className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
          />

          {isSearching && (
            <Loader2 className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 animate-spin" />
          )}

          {query && !isSearching && (
            <button
              type="button"
              onClick={handleClearSearch}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
      </form>

      {/* Search Suggestions */}
      {showSuggestions && showSuggestionsDropdown && suggestions.length > 0 && (
        <div
          ref={dropdownRef}
          className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto"
        >
          <div className="p-2">
            <div className="text-xs font-medium text-gray-500 mb-2 px-2">
              Suggestions
            </div>
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                type="button"
                onClick={() => {
                  setQuery(suggestion);
                  setSearch(suggestion);
                  if (onSearch) {
                    onSearch(suggestion);
                  } else {
                    debouncedSearch(suggestion);
                  }
                  setShowSuggestionsDropdown(false);
                }}
                className="w-full text-left px-2 py-2 text-sm text-gray-700 hover:bg-gray-100 rounded transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
