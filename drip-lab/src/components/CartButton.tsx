'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { ShoppingCart } from 'lucide-react';
import { useCart } from '@/contexts/CartContext';
import ShoppingCartPanel from './ShoppingCart';

interface CartButtonProps {
  className?: string;
}

const CartButton: React.FC<CartButtonProps> = ({ className = '' }) => {
  const [isCartOpen, setIsCartOpen] = useState(false);
  const { totalItems, cartItems, updateQuantity, removeItem } = useCart();

  const checkout = () => {
    // Navigate to checkout page
    console.log('Proceed to checkout');
    setIsCartOpen(false);
  };

  return (
    <>
      <button 
        onClick={() => setIsCartOpen(true)}
        className={`relative p-2 text-foreground hover:text-primary transition-colors ${className}`}
      >
        <ShoppingCart className="w-5 h-5" />
        {totalItems > 0 && (
          <motion.span
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="absolute -top-1 -right-1 bg-primary text-background text-xs rounded-full w-5 h-5 flex items-center justify-center"
          >
            {totalItems}
          </motion.span>
        )}
      </button>

      <ShoppingCartPanel
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        cartItems={cartItems}
        onUpdateQuantity={updateQuantity}
        onRemoveItem={removeItem}
        onCheckout={checkout}
      />
    </>
  );
};

export default CartButton;