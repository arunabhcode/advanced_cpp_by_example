Title: Variadic Templates
Date: 2023-03-02

### Intuition

If you want to write code that can generalize not just across the type but also the number of arguments, you can use variadic templates which serves as a generalization of regular templates

### Explanation

#### Templates

Regular templates can be used to re-use a particular piece of code or a class for different types

	#include <iostream>

	template<typename T>
	void print(const T &value)
	{
		std::cout << value << std::endl;
	}

	int main()
	{
		print(42);
		print("Answers are needed");
		return 0;
	}

#### Variadic Templates

Now generalizing above syntax to number of arguments also, the way to represent a variable number of arguments is the ellipsis operator ..., this variadic argument is then processed recursively until all arguments have been processed.

	#include <iostream>

	// Serves as the base case of the recursion when only one argument is left, 
	// can also be a print statement with no arguments and a do nothing return
	template<typename T>
	void print(const T &value)
	{
		std::cout << value << std::endl;
	}
	// Variadic template based print function
	template<typename T, typename ... Args>
	void print(const T& value, const Args&... args)
	{
		std::cout << value << std::endl;
		print(args...);
	}
	int main()
	{
		print(42, "answers are needed", 3.567);
		print(true, "chatgpt will make us all obsolete in the medium term");
		return 0;
	}

### Application

This concept can be used to implement a logging class by wrapping around an existing log library like the above print function and publish to an object like `std::ostringstream` or directly to console.


### Why is this relevant?

When the constructor or make_xxxxx() functions are called, the number of arguments vary based on the constructor
of the template class for which the smart pointer is instantiated.