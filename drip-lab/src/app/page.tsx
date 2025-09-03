'use client';

import { motion } from 'framer-motion';
import { ArrowRight, Sparkles, Shield, Truck, Headphones } from 'lucide-react';
import HeroSection from '@/components/HeroSection';
import FeaturedProducts from '@/components/FeaturedProducts';
import ProductGrid from '@/components/ProductGrid';
import { Product } from '@/components/ProductCard';
import { useCart } from '@/contexts/CartContext';

export default function Home() {
  const { addToCart } = useCart();

  const viewDetails = (product: Product) => {
    // Navigate to product detail page
    console.log('View details for:', product.name);
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <HeroSection />

      {/* Features Section */}
      <section className="py-16 bg-secondary">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Sparkles className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Handcrafted Excellence</h3>
              <p className="text-muted text-sm">
                Each piece is meticulously crafted by master jewelers with decades of experience.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Authenticity Guaranteed</h3>
              <p className="text-muted text-sm">
                All our jewelry comes with certificates of authenticity and quality assurance.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Truck className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">Free Shipping</h3>
              <p className="text-muted text-sm">
                Complimentary shipping on all orders over $1,000 with insurance included.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <Headphones className="w-8 h-8 text-primary" />
              </div>
              <h3 className="text-lg font-semibold mb-2">24/7 Support</h3>
              <p className="text-muted text-sm">
                Our jewelry experts are available around the clock to assist you.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <FeaturedProducts onAddToCart={addToCart} onViewDetails={viewDetails} />

      {/* All Products */}
      <ProductGrid onAddToCart={addToCart} onViewDetails={viewDetails} />

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-accent to-secondary">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="text-4xl font-bold gradient-text mb-6">
              Ready to Find Your Perfect Piece?
            </h2>
            <p className="text-xl text-muted mb-8">
              Explore our complete collection of handcrafted jewelry, 
              each piece telling its own unique story of luxury and elegance.
            </p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="inline-flex items-center px-8 py-4 bg-primary text-background rounded-lg hover:bg-primary-dark transition-colors font-semibold text-lg"
            >
              Browse Collection
              <ArrowRight className="ml-2 w-5 h-5" />
            </motion.button>
          </motion.div>
        </div>
      </section>


    </div>
  );
}
