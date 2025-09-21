"use client";
import { useState } from "react";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";

const CalendarComponent = () => {
  const [currentMonth, setCurrentMonth] = useState(new Date().getMonth());
  const [currentYear, setCurrentYear] = useState(new Date().getFullYear());
  const [selectedDate, setSelectedDate] = useState(null);

  // Example highlighted dates
  const highlightedDates = {
    yellow: [4],
    outlined: [14],
    black: [30],
  };

  // Get days in the current month
  const getDaysInMonth = (year, month) => {
    return new Date(year, month + 1, 0).getDate();
  };

  const daysInMonth = getDaysInMonth(currentYear, currentMonth);
  const firstDay = new Date(currentYear, currentMonth, 1).getDay(); // 0 = Sunday

  // Handle previous month navigation
  const handlePrevMonth = () => {
    if (currentMonth === 0) {
      setCurrentMonth(11);
    } else {
      setCurrentMonth((prev) => prev - 1);
    }
  };

  // Handle next month navigation
  const handleNextMonth = () => {
    if (currentMonth === 11) {
      setCurrentMonth(0);
    } else {
      setCurrentMonth((prev) => prev + 1);
    }
  };

  return (
    <div className="w-80 p-6 border rounded-lg shadow-lg bg-white">
      <h2 className="text-lg text-gray-800 font-semibold text-center">
        Select a time in the calendar
      </h2>
      
      {/* Month Navigation (Year Removed) */}
      <div className="flex text-gray-600 justify-between items-center mt-3">
        <button onClick={handlePrevMonth} className="p-2 text-gray-600 hover:text-black">
          <FaChevronLeft />
        </button>
        <span className="text-lg font-bold">
          {new Date(currentYear, currentMonth).toLocaleString("default", { month: "long" })}
        </span>
        <button onClick={handleNextMonth} className="p-2 text-gray-600 hover:text-black">
          <FaChevronRight />
        </button>
      </div>

      {/* Calendar Grid */}
      <div className="grid grid-cols-7 gap-1 text-center mt-4">
        {/* Days of the Week (Fix: Added unique keys) */}
        {["M", "T", "W", "T", "F", "S", "S"].map((day, index) => (
          <div key={day + index} className="text-sm font-semibold text-gray-600">
            {day}
          </div>
        ))}

        {/* Empty Cells for First Week */}
        {Array(firstDay === 0 ? 6 : firstDay - 1)
          .fill(null)
          .map((_, index) => (
            <div key={`empty-${index}`}></div>
          ))}

        {/* Dates in Month */}
        {Array.from({ length: daysInMonth }, (_, i) => {
          const day = i + 1;
          let style = "p-2 rounded-full cursor-pointer text-gray-800 hover:bg-gray-200";

          // Highlighted Dates
          if (highlightedDates.yellow.includes(day)) {
            style += " bg-yellow-300 text-black";
          } else if (highlightedDates.outlined.includes(day)) {
            style += " border border-black";
          } else if (highlightedDates.black.includes(day)) {
            style += " bg-black text-white";
          }

          return (
            <div
              key={`date-${day}`}
              className={`flex items-center justify-center w-10 h-10 ${style} ${
                selectedDate === day ? "bg-teal-500 text-white" : ""
              }`}
              onClick={() => setSelectedDate(day)}
            >
              {day}
            </div>
          );
        })}
      </div>

      {/* Button */}
      <button className="w-full bg-teal-500 text-white text-center py-2 mt-5 rounded-md hover:bg-teal-600">
        Message to landlord
      </button>
    </div>
  );
};

export default CalendarComponent;