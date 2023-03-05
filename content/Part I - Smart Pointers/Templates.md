Title: Templates
Date: 2023-03-02

### Intuition

If you want to write code which can generalize across type of the argument/object, you can use a templates.

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

### Why is this relevant?

You can use templates to implement a basic shared_ptr like class for basic POD(plain old data) types.

	#include <iostream>
	
	namespace toy
	{
		template <typename T>
		class SharedPtr
		{
		  public:
			explicit SharedPtr(const T& value) : data(new T(value)), ref_count(new size_t(1))
			{
			}

			SharedPtr(const SharedPtr<T>& other) : data(other.data), ref_count(other.ref_count)
			{
			  // If ref_count > 0 then augment ref_count which means there are already pointers to the underlying data
			  if (ref_count)
			  {
			    (*ref_count)++;
			  }
			}

			~SharedPtr()
			{

			  if (ref_count)
			  {
			    (*ref_count)--;
			    // If ref_count reaches zero after this destructor call, delete data and ref_count
			    if (*ref_count == 0)
			    {
			      delete data;
			      delete ref_count;
			    }
			    data      = nullptr;
			    ref_count = nullptr;
			  }
			}

			T& operator*() const
			{
			  return *data;
			}

		  	T* get() const
		  	{
		  	  return data;
		  	}
		
		 private:
		  	T* data;
		  	size_t* ref_count;
		};
	}  // namespace toy
	
	int main()
	{
	  toy::SharedPtr<int> test_ptr(10);
	  std::cout << test_ptr.get() << std::endl;
	  return 0;
	}