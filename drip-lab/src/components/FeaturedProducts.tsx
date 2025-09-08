'use client';

import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import ProductCard, { Product } from './ProductCard';
import { products } from '@/data/products';

interface FeaturedProductsProps {
  onAddToCart: (product: Product) => void;
  onViewDetails: (product: Product) => void;
}

const FeaturedProducts: React.FC<FeaturedProductsProps> = ({ 
  onAddToCart, 
  onViewDetails 
}) => {
  // Get featured products (highest rated)
  const featuredProducts = products
    .sort((a, b) => b.rating - a.rating)
    .slice(0, 6);

  return (
    <section className="py-20 bg-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold gradient-text mb-6">
            Featured Collection
          </h2>
          <p className="text-xl text-muted max-w-3xl mx-auto">
            Discover our most beloved pieces, handpicked for their exceptional craftsmanship 
            and timeless beauty. Each piece tells a story of luxury and elegance.
          </p>
        </motion.div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
          {featuredProducts.map((product, index) => (
            <motion.div
              key={product.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ 
                duration: 0.6, 
                delay: index * 0.1 
              }}
              viewport={{ once: true }}
            >
              <ProductCard
                product={product}
                onAddToCart={onAddToCart}
                onViewDetails={onViewDetails}
              />
            </motion.div>
          ))}
        </div>

        {/* View All Button */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="text-center"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="inline-flex items-center px-8 py-4 bg-transparent border-2 border-primary text-primary rounded-lg hover:bg-primary hover:text-background transition-colors font-semibold text-lg"
          >
            View All Products
            <ArrowRight className="ml-2 w-5 h-5" />
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
};

export default FeaturedProducts;