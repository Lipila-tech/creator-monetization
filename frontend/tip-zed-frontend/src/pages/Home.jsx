import { useState } from 'react'
import { Link } from 'react-router-dom' // Import Link for navigation

const Home = () => {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen min-w-screen bg-gray-50 flex flex-col items-center justify-center px-4 py-8 md:py-16">
      
      {/* Header */}
      <header className="mb-8 md:mb-12 text-center max-w-xl md:max-w-3xl">
        <h1 className="text-3xl sm:text-4xl md:text-6xl font-bold text-zed-green mb-2">
          Tip Zed
        </h1>

        <div className="flex justify-center gap-1 sm:gap-2 mb-3 md:mb-5">
          <div className="h-2 w-10 sm:w-14 md:w-20 bg-zed-green rounded-full"></div>
          <div className="h-2 w-10 sm:w-14 md:w-20 bg-zed-red rounded-full"></div>
          <div className="h-2 w-10 sm:w-14 md:w-20 bg-zed-black rounded-full"></div>
          <div className="h-2 w-10 sm:w-14 md:w-20 bg-zed-orange rounded-full"></div>
        </div>

        <p className="text-gray-600 text-sm sm:text-base md:text-lg px-2">
          The easiest way to support Zambian creators.
        </p>
      </header>

      {/* Main Card */}
      <div className="bg-white w-full max-w-sm sm:max-w-md md:max-w-2xl lg:max-w-4xl p-6 sm:p-8 md:p-10 rounded-2xl shadow-lg md:shadow-xl border-t-4 border-zed-orange">
        <div className="text-center space-y-4">
          
          <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
            <Link 
              to="/login" 
              className="bg-zed-green hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition-all"
            >
              Login
            </Link>
            <Link 
              to="/register" 
              className="bg-white border-2 border-zed-orange text-zed-orange hover:bg-orange-50 font-bold py-3 px-6 rounded-lg transition-all"
            >
              Sign Up
            </Link>
          </div>

          <p className="mt-4 text-xs sm:text-sm text-gray-500">
            Day 1 Setup Complete.
          </p>
        </div>
      </div>
    </div>
  )
}

export default Home