Title: Type traits
Date: 2023-03-13

### Intuition

Building on the intuition of variadic templates, where we generalized across types and the number of arguments there are a couple of ways to think about type traits:
(1) While in templates, we instantiated/specialized entire functions or classes to a single type or value, type traits help give us more granular control where we can choose to execute a few lines of code based on the type as opposed to a binary either entire function gets executed or not.
(2) Second intuition is connected to what type traits are which is properties of the types themselves so in the sense the typename itself is the variable(very meta!) to be checked or manipulated(at compile time).

### Explanation

In practice, type traits end up being templated structs that help to do any of the following things and usually contain one or both of these two members:

#### Type Properties

(1) the "value" member which is a compile-time constant that answers questions about aspects of the type like `is_integral`, `is_floating_point`, `is_copy_constructible`.

Example of usage of above:

	#include <iostream>
	#include <type_traits>

	struct Test {};

	int main()
	{
		std::cout << std::is_integral<int>::value << std::endl;
		std::cout << std::is_floating_point<int>::value << std::endl;
		std::cout << std::is_copy_constructible<Test>::value << std::endl;
		return 0;
	}

	
Let's implement our own trait called `is_printable` for the previous log class: 

	#include <iostream>
	#include <type_traits>

	struct Test {};

	template<typename T>
	struct is_printable {
	private:
	    template<typename U>
	    static decltype(std::cout << std::declval<U>(), std::true_type{}) _is_printable_helper(int);
	
	    template<typename U>
	    static std::false_type _is_printable_helper(...);
	
	public:
	    static const bool value = decltype(_is_printable_helper<T>(0))::value;
	};
	
	int main()
	{
		std::cout << std::boolalpha;
		std::cout << is_printable<int>::value << std::endl;
		std::cout << is_printable<Test>::value << std::endl;
		return 0;
	}

	

#### Type Manipulation   

(2) the "type" member which is a typename generated after type manipulations like `remove_const`, `remove_pointer`, `remove_reference`.

	#include <iostream>
	#include <type_traits>
	#include <typeinfo>
	#include <cxxabi.h>

	int main()
	{
		int status;
    	char* intp_name = abi::__cxa_demangle(typeid(int*).name(), nullptr, nullptr, &status);
		std::cout << intp_name << std::endl;
    	char* int_name = abi::__cxa_demangle(typeid(std::remove_pointer<int*>::type).name(), nullptr, nullptr, &status);
		std::cout << int_name << std::endl;
		return 0;
	}


Practical example of how std::move uses this to turn `T` into `T&&`:

	namespace std
	{
		template <typename T>
		typename std::remove_reference<T>::type&& move(T&& val) noexcept
		{
		    return static_cast<typename std::remove_reference<T>::type&&>(val);
		}	
	}



#### Conditional Compilation

The members above can then be used to wield more fine control over what parts of the code to execute based on the typename itself almost like a compile time if-else.
Let's do conditional compilation a couple of ways, one using `std::enable_if` and second using `if constexpr`.

(1) `std::enable_if`:

	#include <iostream>
	#include <type_traits>
	
	template <typename T>
	typename std::enable_if<!std::is_pointer<typename std::remove_reference<T>::type>::value, void>::type print(T&& t)
	{
	    std::cout << t << std::endl;
	}

	template <typename T>
	typename std::enable_if<std::is_pointer<typename std::remove_reference<T>::type>::value, void>::type print(T&& t)
	{
	    std::cout << *t << std::endl;
	}

	int main()
	{
	    int a = 1;
	    print(a);
	
	    int* b = new int(2);
	    print(b);
	    delete b;
	
	    return 0;
	}

(2) `if_constexpr`:	

	#include <iostream>
	#include <type_traits>
	#include <typeinfo>
	#include <cxxabi.h>

	struct Test {};

	template<typename T>
	struct is_printable {
	private:
	    template<typename U>
	    static decltype(std::cout << std::declval<U>(), std::true_type{}) _is_printable_helper(int);
	
	    template<typename U>
	    static std::false_type _is_printable_helper(...);
	
	public:
	    static constexpr bool value = decltype(_is_printable_helper<T>(0))::value;
	};

	void print()
	{
		return;
	}

	// Variadic template based print function
	template<typename T, typename ... Args>
	void print(const T& val, const Args&... args)
	{
		if constexpr(is_printable<T>::value)
		{
			std::cout << val << std::endl;
		}
		else
		{
			int status;
    		char* t_name = abi::__cxa_demangle(typeid(T).name(), nullptr, nullptr, &status);
			std::cout << "Object of type = " << t_name << " is not printable" << std::endl;	
		}
		print(args...);
	}

	int main()
	{
		int a = 4;
		float b = 6.3f;
		Test c;
		print(a, b, c);
		return 0;
	}



### Why is this relevant?

This is relevant because `remove_reference` is used inside the context of `make_shared` indirectly.
	
	#include <iostream>
	#include <type_traits>

	template <typename T>
	struct remove_reference
	{	 
		using type = T; 
	};

	template <typename T>
	struct remove_reference<T&> 
	{
	    using type = T;
	};

	template <typename T>
	struct remove_reference<T&&> 
	{
	    using type = T;
	};

	int main()
	{
		std::cout << std::boolalpha;
		std::cout << std::is_same<int, int&>::value << std::endl;
		std::cout << std::is_same<int, remove_reference<int&>::type>::value << std::endl;
		std::cout << std::is_same<int, int&&>::value << std::endl;
		std::cout << std::is_same<int, remove_reference<int&&>::type>::value << std::endl;
		return 0;
	}

