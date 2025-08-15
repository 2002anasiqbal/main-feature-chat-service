"use client";
import React, { useState } from 'react';
import { ChevronRight, ChevronLeft, Plus, Minus, CreditCard } from 'lucide-react';
import { useRouter } from 'next/navigation';

// Cart Item Component
const CartItem = ({ item, updateQuantity, removeItem }) => {
  return (
    <div className="flex items-center py-4 border-b">
      <div className="flex-shrink-0 w-24 h-24">
        <img src={item.image} alt={item.name} className="w-full h-full object-cover" />
      </div>
      <div className="ml-4 flex-grow">
        <h3 className="text-lg font-semibold text-gray-800">{item.name}</h3>
        <p className="text-gray-800">Color: {item.color}</p>
        <div className="flex items-center mt-3">
          <button
            className="p-1 border rounded"
            onClick={() => updateQuantity(item.id, item.quantity - 1)}
          >
            <Minus size={16} className="text-gray-800" />
          </button>
          <span className="mx-3 text-gray-800">{item.quantity}</span>
          <button
            className="p-1 border rounded"
            onClick={() => updateQuantity(item.id, item.quantity + 1)}
          >
            <Plus size={16} className="text-gray-800" />
          </button>
          <button
            className="ml-6 text-gray-800"
            onClick={() => removeItem(item.id)}
          >
            Remove
          </button>
        </div>
      </div>
      <div className="text-right">
        <span className="text-lg font-bold text-gray-800">${item.price.toFixed(2)}</span>
      </div>
    </div>
  );
};

// Cart Step Component (Step 0)
const CartStep = ({ cartItems, updateQuantity, removeItem }) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">
        Cart <span className="text-sm font-normal text-gray-800">{cartItems.length} ITEMS</span>
      </h2>
      {cartItems.map(item => (
        <CartItem 
          key={item.id} 
          item={item} 
          updateQuantity={updateQuantity} 
          removeItem={removeItem} 
        />
      ))}
      <div className="p-4 border rounded-md bg-blue-50 flex items-center">
        <div className="flex-shrink-0 mr-2 text-gray-800">%</div>
        <div className="text-gray-800">
          10% Instant Discount with Federal Bank Debit Cards on a min spend of $150. T&C Apply
        </div>
      </div>
    </div>
  );
};

// Address Step Component (Step 1)
const AddressStep = ({ addresses, selectAddress }) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Address</h2>
      {addresses.map(addr => (
        <div
          key={addr.id}
          className={`p-4 border rounded-md ${addr.isSelected ? 'border-teal-500' : ''}`}
          onClick={() => selectAddress(addr.id)}
        >
          <div className="flex items-center">
            <input
              type="radio"
              checked={addr.isSelected}
              onChange={() => selectAddress(addr.id)}
              className="mr-2"
            />
            <span className="font-bold text-gray-800">{addr.name}</span>
            <span className="ml-2 text-xs bg-teal-100 text-gray-800 px-1 rounded">{addr.type}</span>
            <div className="ml-auto">
              <button className="mr-4 text-gray-800">Edit</button>
              <button className="text-gray-800">Remove</button>
            </div>
          </div>
          <div className="ml-5 mt-2">
            <p className="text-gray-800">{addr.address}</p>
            <p className="mt-1 text-gray-800">Contact - {addr.contact}</p>
          </div>
        </div>
      ))}
      <button className="flex items-center text-gray-800 font-medium">
        <Plus size={16} className="mr-2 text-gray-800" />
        Add New Address
      </button>
    </div>
  );
};

// Shipping Step Component (Step 2)
const ShippingStep = ({ shippingMethods, selectShipping }) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Shipment Method</h2>
      <div className="border rounded-md overflow-hidden">
        {shippingMethods.map(method => (
          <div
            key={method.id}
            className={`p-4 flex items-center border-b ${method.isSelected ? 'bg-gray-50' : ''}`}
            onClick={() => selectShipping(method.id)}
          >
            <input
              type="radio"
              checked={method.isSelected}
              onChange={() => selectShipping(method.id)}
              className="mr-3"
            />
            <div className="flex-grow">
              <div className="flex items-center">
                <span className={`font-${method.price === null ? 'normal' : 'bold'} text-gray-800`}>
                  {method.price === null
                    ? ""
                    : method.price === 0
                    ? "Free"
                    : `$${method.price.toFixed(2)}`}
                </span>
                <span className="ml-3 text-gray-800">{method.name}</span>
              </div>
            </div>
            <div className="text-right">
              {method.date ? 
                <span className="text-gray-800">{method.date}</span> :
                <button className="flex items-center text-gray-800">
                  Select Date <ChevronRight size={16} className="text-gray-800" />
                </button>
              }
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Payment Step Component (Step 3)
const PaymentStep = ({ paymentMethods, selectPayment }) => {
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Payment Method</h2>
      <div className="space-y-3">
        {paymentMethods.map(method => (
          <div
            key={method.id}
            className="p-4 border rounded-md flex items-center"
            onClick={() => selectPayment(method.id)}
          >
            <input
              type="radio"
              checked={method.isSelected}
              onChange={() => selectPayment(method.id)}
              className="mr-3"
            />
            <div className="flex items-center">
              <div className="w-8 h-5 bg-blue-500 rounded mr-2"></div>
              <span className="text-gray-800">•••• {method.last4}</span>
              <span className="ml-6 text-gray-800">Expires {method.expires}</span>
            </div>
            <button className="ml-auto text-gray-800">Remove</button>
          </div>
        ))}
      </div>
      <button className="flex items-center text-gray-800 font-medium">
        <Plus size={16} className="mr-2 text-gray-800" />
        Add Payment method
      </button>
    </div>
  );
};

// Order Confirmation Component (final view after placing order)
const OrderConfirmation = ({ getSelectedShipping, resetCart }) => {
  const router = useRouter();
  const handleContinueShopping = () => {
    resetCart();
    router.back(); // Navigates to the last visited page (where user clicked cart)
  };

  return (
    <div className="text-center py-8">
      <div className="text-2xl font-bold text-gray-800 mb-4">Order Placed</div>
      <p className="text-gray-800">Your order has been placed successfully!</p>
      <p className="text-gray-800">Estimated delivery: {getSelectedShipping().date}</p>
      <button
        className="mt-6 px-6 py-3 bg-teal-500 text-white rounded-md"
        onClick={handleContinueShopping}
      >
        Continue Shopping
      </button>
    </div>
  );
};

// Order Summary Component
const OrderSummary = ({ totals, getSelectedShipping, nextStep, currentStep, steps, orderPlaced }) => {
  return (
    <div className="border rounded-md p-5">
      <h3 className="text-xl font-bold mb-5 text-gray-800">Order Summary</h3>
      <div className="space-y-3">
        <div className="flex justify-between">
          <span className="text-gray-800">Price</span>
          <span className="text-gray-800">${totals.price}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-800">Discount</span>
          <span className="text-gray-800">${totals.discount}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-800">Shipping</span>
          <span className="text-gray-800">{totals.shipping}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-800">Coupon Applied</span>
          <span className="text-gray-800">${totals.coupon.toFixed(2)}</span>
        </div>
        <div className="border-t my-3"></div>
        <div className="flex justify-between font-bold">
          <span className="text-gray-800">TOTAL</span>
          <span className="text-gray-800">${totals.total}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-gray-800">Estimated Delivery by</span>
          <span className="text-gray-800">{getSelectedShipping()?.date || "01 Feb, 2023"}</span>
        </div>
        {/* Coupon Code Input Container */}
        <div className="mt-4 flex border rounded overflow-hidden">
          <input
            type="text"
            placeholder="Coupon Code"
            className="flex-grow p-3 outline-none text-gray-800 min-w-0"
          />
          <button className="flex-none p-3">
            <CreditCard className="text-gray-800" />
          </button>
        </div>
        <button
          onClick={nextStep}
          className="w-full py-3 bg-teal-500 text-white rounded-md mt-4"
        >
          {orderPlaced
            ? "Order Placed"
            : currentStep === 0
            ? "Proceed to Checkout"
            : currentStep === steps.length - 1
            ? "Place Your Order and Pay"
            : `Continue to ${steps[currentStep + 1]}`}
        </button>
      </div>
    </div>
  );
};

// Progress Bar Component
const ProgressBar = ({ steps, currentStep }) => {
  return (
    <div className="flex items-center mb-8">
      {steps.map((step, index) => (
        <React.Fragment key={step}>
          <div className="flex flex-col items-center">
            <div
              className={`h-8 w-8 rounded-full flex items-center justify-center ${
                index <= currentStep ? 'bg-teal-500 text-white' : 'bg-gray-200'
              }`}
            >
              {index < currentStep ? '✓' : index + 1}
            </div>
            <span className={`mt-1 text-sm text-gray-800`}>{step}</span>
          </div>
          {index < steps.length - 1 && (
            <div className={`flex-grow h-1 mx-2 ${index < currentStep ? 'bg-teal-500' : 'bg-gray-200'}`}></div>
          )}
        </React.Fragment>
      ))}
    </div>
  );
};

// Main Shopping Cart Component that always starts from the Cart (checkout) page
const ShoppingCartComponent = () => {
  const router = useRouter();
  // Checkout steps
  const steps = ["Cart", "Address", "Shipping", "Payment"];
  const [currentStep, setCurrentStep] = useState(0);
  const [orderPlaced, setOrderPlaced] = useState(false);

  // Initial Cart Data (pre-populated)
  const [cartItems, setCartItems] = useState([
    {
      id: 1,
      name: "iPhone",
      color: "Gunnared biege",
      price: 149.99,
      quantity: 1,
      image: "/api/placeholder/120/120"
    },
    {
      id: 2,
      name: "iPhone",
      color: "Lysed bright green",
      price: 169.99,
      quantity: 1,
      image: "/api/placeholder/120/120"
    }
  ]);

  // Address data
  const [addresses, setAddresses] = useState([
    {
      id: 1,
      name: "Huzefa Bagwala",
      type: "HOME",
      address: "1131 Dusty Townline, Jacksonville, TX 40322",
      contact: "(936) 361-0310",
      isSelected: true
    },
    {
      id: 2,
      name: "Johar Town",
      type: "OFFICE",
      address: "1219 Harvest Path, Jacksonville, TX 40326",
      contact: "(936) 361-0310",
      isSelected: false
    }
  ]);

  // Shipping methods
  const [shippingMethods, setShippingMethods] = useState([
    {
      id: 1,
      name: "Regular Shipment",
      price: 0,
      date: "01 Feb, 2023",
      isSelected: true
    },
    {
      id: 2,
      name: "Priority Shipping",
      price: 8.50,
      date: "28 Jan, 2023",
      isSelected: false
    },
    {
      id: 3,
      name: "Choose a date that works for you.",
      price: null,
      date: null,
      isSelected: false
    }
  ]);

  // Payment methods
  const [paymentMethods, setPaymentMethods] = useState([
    {
      id: 1,
      last4: "6754",
      type: "visa",
      expires: "06/2021",
      isSelected: true
    },
    {
      id: 2,
      last4: "5643",
      type: "mastercard",
      expires: "11/2025",
      isSelected: false
    }
  ]);

  // Helper functions for cart management
  const updateQuantity = (id, newQuantity) => {
    if (newQuantity < 1) return;
    setCartItems(cartItems.map(item =>
      item.id === id ? { ...item, quantity: newQuantity } : item
    ));
  };

  const removeItem = (id) => {
    setCartItems(cartItems.filter(item => item.id !== id));
  };

  // Helper functions for address, shipping, and payment selection
  const selectAddress = (id) => {
    setAddresses(addresses.map(addr => ({ ...addr, isSelected: addr.id === id })));
  };

  const selectShipping = (id) => {
    setShippingMethods(shippingMethods.map(method => ({ ...method, isSelected: method.id === id })));
  };

  const selectPayment = (id) => {
    setPaymentMethods(paymentMethods.map(method => ({ ...method, isSelected: method.id === id })));
  };

  const getSelectedShipping = () => shippingMethods.find(method => method.isSelected);

  // Navigation functions
  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      setOrderPlaced(true);
    }
  };

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const resetCart = () => {
    setCartItems([]);
    setCurrentStep(0);
    setOrderPlaced(false);
  };

  // Calculate order summary
  const calculateTotals = () => {
    const subtotal = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const discount = subtotal * 0.1;
    const shipping = getSelectedShipping()?.price || 0;
    const total = subtotal - discount + shipping;
    return {
      subtotal: subtotal.toFixed(2),
      price: subtotal.toFixed(2),
      discount: discount.toFixed(1),
      shipping: shipping === 0 ? "Free" : `$${shipping.toFixed(2)}`,
      coupon: 0.00,
      total: total.toFixed(2)
    };
  };

  // Render the checkout view based on the current step
  const renderCheckoutView = () => {
    if (orderPlaced) {
      return (
        <div className="max-w-md mx-auto">
          <OrderSummary 
            totals={calculateTotals()} 
            getSelectedShipping={getSelectedShipping} 
            nextStep={nextStep} 
            currentStep={currentStep} 
            steps={steps} 
            orderPlaced={orderPlaced} 
          />
          <OrderConfirmation 
            getSelectedShipping={getSelectedShipping} 
            resetCart={resetCart} 
          />
        </div>
      );
    }

    return (
      <div>
        {/* Back arrow: on Cart step, use router.back(); on other steps, use prevStep */}
        <button
          onClick={currentStep === 0 ? () => router.back() : prevStep}
          className="flex items-center text-gray-800 mb-4"
        >
          <ChevronLeft size={20} className="mr-1" /> Back
        </button>
        <div className="flex flex-col md:flex-row gap-6">
          <div className="md:w-2/3">
            {currentStep > 0 && <ProgressBar steps={steps} currentStep={currentStep} />}
            {currentStep === 0 && 
              <CartStep 
                cartItems={cartItems} 
                updateQuantity={updateQuantity} 
                removeItem={removeItem} 
              />
            }
            {currentStep === 1 && 
              <AddressStep 
                addresses={addresses} 
                selectAddress={selectAddress} 
              />
            }
            {currentStep === 2 && 
              <ShippingStep 
                shippingMethods={shippingMethods} 
                selectShipping={selectShipping} 
              />
            }
            {currentStep === 3 && 
              <PaymentStep 
                paymentMethods={paymentMethods} 
                selectPayment={selectPayment} 
              />
            }
          </div>
          <div className="md:w-1/3">
            <OrderSummary 
              totals={calculateTotals()} 
              getSelectedShipping={getSelectedShipping} 
              nextStep={nextStep} 
              currentStep={currentStep} 
              steps={steps} 
              orderPlaced={orderPlaced} 
            />
          </div>
        </div>
      </div>
    );
  };

  // Always render the checkout view starting from the Cart step
  return (
    <div className="max-w-6xl mx-auto px-4">
      {renderCheckoutView()}
    </div>
  );
};

export default ShoppingCartComponent;
