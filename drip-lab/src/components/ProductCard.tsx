'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Heart, ShoppingCart, Eye } from 'lucide-react';
import Jewelry3D from './Jewelry3D';

export interface Product {
  id: string;
  name: string;
  price: number;
  originalPrice?: number;
  description: string;
  category: 'ring' | 'necklace' | 'earrings' | 'bracelet';
  material: 'gold' | 'silver' | 'platinum';
  image: string;
  inStock: boolean;
  rating: number;
  reviews: number;
  tags: string[];
}

interface ProductCardProps {
  product: Product;
  onAddToCart: (product: Product) => void;
  onViewDetails: (product: Product) => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ 
  product, 
  onAddToCart, 
  onViewDetails 
}) => {
  const [isHovered, setIsHovered] = useState(false);
  const [isLiked, setIsLiked] = useState(false);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const renderStars = (rating: number) => {
    return Array.from({ length: 5 }, (_, i) => (
      <span
        key={i}
        className={`text-sm ${
          i < Math.floor(rating) ? 'text-gold' : 'text-muted'
        }`}
      >
        ★
      </span>
    ));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5 }}
      transition={{ duration: 0.3 }}
      className="bg-secondary rounded-lg overflow-hidden border border-border hover:border-primary/50 transition-all duration-300 group"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* 3D Preview */}
      <div className="relative h-64 bg-gradient-to-br from-accent to-secondary">
        <Jewelry3D 
          jewelryType={product.category} 
          material={product.material}
          className="w-full h-full"
        />
        
        {/* Overlay Actions */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: isHovered ? 1 : 0 }}
          className="absolute inset-0 bg-black/50 flex items-center justify-center space-x-4"
        >
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => onViewDetails(product)}
            className="p-3 bg-primary text-background rounded-full hover:bg-primary-dark transition-colors"
          >
            <Eye className="w-5 h-5" />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => onAddToCart(product)}
            className="p-3 bg-background text-foreground rounded-full hover:bg-accent transition-colors"
          >
            <ShoppingCart className="w-5 h-5" />
          </motion.button>
        </motion.div>

        {/* Wishlist Button */}
        <button
          onClick={() => setIsLiked(!isLiked)}
          className="absolute top-4 right-4 p-2 bg-background/80 backdrop-blur-sm rounded-full hover:bg-background transition-colors"
        >
          <Heart 
            className={`w-4 h-4 transition-colors ${
              isLiked ? 'text-red-500 fill-red-500' : 'text-foreground'
            }`} 
          />
        </button>

        {/* Sale Badge */}
        {product.originalPrice && (
          <div className="absolute top-4 left-4 bg-red-500 text-white text-xs px-2 py-1 rounded-full">
            Sale
          </div>
        )}

        {/* Out of Stock Overlay */}
        {!product.inStock && (
          <div className="absolute inset-0 bg-black/70 flex items-center justify-center">
            <span className="text-white font-semibold">Out of Stock</span>
          </div>
        )}
      </div>

      {/* Product Info */}
      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">
            {product.name}
          </h3>
          <span className="text-xs text-muted uppercase bg-accent px-2 py-1 rounded">
            {product.material}
          </span>
        </div>

        <p className="text-muted text-sm mb-3 line-clamp-2">
          {product.description}
        </p>

        {/* Rating */}
        <div className="flex items-center space-x-2 mb-3">
          <div className="flex">
            {renderStars(product.rating)}
          </div>
          <span className="text-xs text-muted">
            ({product.reviews} reviews)
          </span>
        </div>

        {/* Price */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-lg font-bold text-primary">
              {formatPrice(product.price)}
            </span>
            {product.originalPrice && (
              <span className="text-sm text-muted line-through">
                {formatPrice(product.originalPrice)}
              </span>
            )}
          </div>
          
          <button
            onClick={() => onAddToCart(product)}
            disabled={!product.inStock}
            className="px-4 py-2 bg-primary text-background rounded-lg hover:bg-primary-dark disabled:bg-muted disabled:cursor-not-allowed transition-colors text-sm font-medium"
          >
            {product.inStock ? 'Add to Cart' : 'Sold Out'}
          </button>
        </div>

        {/* Tags */}
        {product.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-3">
            {product.tags.slice(0, 3).map((tag) => (
              <span
                key={tag}
                className="text-xs text-muted bg-accent px-2 py-1 rounded"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
};

export default ProductCard;