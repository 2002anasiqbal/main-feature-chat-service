"use client";
import React, { useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { FiArrowLeft, FiArrowRight } from "react-icons/fi";
import { FaArrowLeft } from "react-icons/fa";

// ✅ Generic Product Detail Component
const ProductMoreDeatils = ({
    title = "Meryl Lounge Chair",
    price = 149.99,
    currency = "$",
    rating = 4.6,
    totalReviews = 556,
    description = "The gently curved lines accentuated by sewn details are kind to your body and pleasant to look at.",
    colors = ["#A8C4B1", "#C5B8B4", "#D6D6D6"],
    productImages = [
        "/default-product.jpg",
        "/default-product-side.jpg",
        "/default-product-back.jpg",
    ],
    seller = {
        name: "Alexa Rawles",
        email: "alexarawles@gmail.com",
        partnerLink: "#",
        sellerInfo: "This is how we choose a seller",
    },
    onBuyClick = () => alert("Buying product..."),
}) => {
    const router = useRouter();
    const [currentImage, setCurrentImage] = useState(0);

    // Image Navigation Handlers
    const nextImage = () => setCurrentImage((prev) => (prev + 1) % productImages.length);
    const prevImage = () => setCurrentImage((prev) => (prev === 0 ? productImages.length - 1 : prev - 1));

    return (
        <div className=" p-6 lg:p-12 bg-white shadow-lg rounded-lg border border-gray-200">
            {/* 🔙 Back Button */}
            <button className="flex items-center text-gray-700 hover:text-black font-medium mb-6" onClick={() => router.back()}>
                <FaArrowLeft className="mr-2" /> Back
            </button>

            {/* 📌 Main Product Section */}
            <div className="grid grid-cols-1 lg:grid-cols-[50%_50%] gap-10">
                {/* 🖼️ Product Image Section */}
                <div className="relative">
                    <Image
                        src={productImages[currentImage]}
                        alt={title}
                        width={500}
                        height={400}
                        className="rounded-lg object-cover w-full border"
                    />
                    <div className="absolute top-3 right-3 bg-black text-white px-3 py-1 text-sm rounded-lg shadow-md">
                        <span className="font-semibold">{currentImage + 1}</span> / {productImages.length}
                    </div>

                    {/* 🔄 Image Navigation */}
                    <button onClick={prevImage} className="absolute left-3 top-1/2 transform -translate-y-1/2 p-3 bg-white shadow-md rounded-full hover:bg-gray-100">
                        <FiArrowLeft size={22} />
                    </button>
                    <button onClick={nextImage} className="absolute right-3 top-1/2 transform -translate-y-1/2 p-3 bg-white shadow-md rounded-full hover:bg-gray-100">
                        <FiArrowRight size={22} />
                    </button>

                    {/* 📌 Thumbnail Images */}
                    <div className="flex mt-3 justify-center gap-3">
                        {productImages.map((img, index) => (
                            <div
                                key={index}
                                className={`w-16 h-16 border rounded-lg overflow-hidden cursor-pointer transition ${
                                    currentImage === index ? "border-teal-500" : "border-gray-300"
                                }`}
                                onClick={() => setCurrentImage(index)}
                            >
                                <Image src={img} alt="thumbnail" width={64} height={64} className="object-cover w-full h-full" />
                            </div>
                        ))}
                    </div>
                </div>

                {/* ℹ️ Product Information */}
                <div className="space-y-6">
                    <h1 className="text-3xl lg:text-4xl font-bold text-gray-900">{title}</h1>

                    {/* 💲 Pricing */}
                    <div className="text-gray-700 text-lg">
                        <p className="text-2xl font-bold text-black">{currency} {price}</p>
                        <p className="text-yellow-500 font-medium flex items-center">
                            ⭐ {rating} / 5.0 <span className="text-gray-500 ml-1">({totalReviews})</span>
                        </p>
                    </div>

                    {/* 🎨 Color Variants */}
                    <div className="flex items-center gap-3">
                        {colors.map((color, index) => (
                            <div key={index} className="w-6 h-6 rounded-full border-2 cursor-pointer" style={{ backgroundColor: color }}></div>
                        ))}
                    </div>

                    {/* 🛒 Buy Button */}
                    <button onClick={onBuyClick} className="px-6 py-3 bg-teal-600 text-white rounded-lg text-lg font-medium hover:bg-teal-700 transition">
                        Buy with fix done
                    </button>

                    {/* 📝 Description */}
                    <div>
                        <h3 className="text-lg font-semibold text-gray-800">Description</h3>
                        <p className="text-gray-700">{description}</p>
                    </div>
                </div>
            </div>

            {/* 📍 Seller Info Section */}
            <div className="mt-10 border-t pt-6 flex flex-col md:flex-row justify-between items-start">
                {/* 📝 Seller Information */}
                <div className="w-full md:w-3/4 space-y-4">
                    <h3 className="text-2xl font-bold text-gray-900">Safe Trading</h3>
                    <p className="text-gray-700">
                        The item is sent to you and you have 24 hours to inspect it before the money is transferred to the seller.
                    </p>
                </div>

                {/* 🏪 Seller Contact Card */}
                <div className="w-full md:w-1/4 bg-gray-50 shadow-md p-4 rounded-lg border">
                    <h3 className="text-lg font-semibold text-gray-900">Contact with Seller</h3>
                    <p className="text-sm text-gray-600">{seller.email}</p>

                    {/* 🔗 Seller Links */}
                    <div className="mt-2">
                        <a href={seller.partnerLink} target="_blank" className="block text-teal-600 hover:underline">Sold by our Partner</a>
                        <a href={seller.sellerInfo} target="_blank" className="block text-teal-600 hover:underline">This is how we choose a seller</a>
                    </div>

                    {/* 📩 Contact Seller Button */}
                    <button onClick={() => alert("Messaging Seller...")} className="w-full mt-4 px-5 py-2 bg-teal-600 text-white rounded-md font-medium hover:bg-teal-700 transition">
                        Send Message
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ProductMoreDeatils;