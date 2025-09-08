'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Menu, X, Search, User } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import CartButton from './CartButton';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Rings', href: '/rings' },
    { name: 'Necklaces', href: '/necklaces' },
    { name: 'Earrings', href: '/earrings' },
    { name: 'Bracelets', href: '/bracelets' },
    { name: 'Collections', href: '/collections' },
  ];

  return (
    <header className="sticky top-0 z-50 glass border-b border-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-gold to-primary rounded-lg flex items-center justify-center">
              <span className="text-background font-bold text-lg">D</span>
            </div>
            <span className="text-xl font-bold gradient-text">Drip Lab</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className="text-foreground hover:text-primary transition-colors duration-200 font-medium"
              >
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Right side actions */}
          <div className="flex items-center space-x-4">
            {/* Search */}
            <button className="p-2 text-foreground hover:text-primary transition-colors">
              <Search className="w-5 h-5" />
            </button>

            {/* User Account */}
            <button className="p-2 text-foreground hover:text-primary transition-colors">
              <User className="w-5 h-5" />
            </button>

            {/* Shopping Cart */}
            <CartButton />

            {/* Mobile menu button */}
            <button
              className="md:hidden p-2 text-foreground hover:text-primary transition-colors"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <AnimatePresence>
          {isMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden border-t border-border"
            >
              <nav className="py-4 space-y-2">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    className="block px-4 py-2 text-foreground hover:text-primary hover:bg-accent rounded-lg transition-colors duration-200"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    {item.name}
                  </Link>
                ))}
              </nav>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </header>
  );
};

export default Header;