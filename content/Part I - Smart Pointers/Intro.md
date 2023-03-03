Title: Introduction to smart pointers
Date: 2023-03-01

### Intuition
Smart pointers were created as wrappers around raw pointers to deal with two of the most common memory management problems:
(i) Failing to deallocate memory appropriately leading to memory leaks
(ii) Trying to access/deallocate already deallocated memory

### Explanation

In order these problems, there exist 3 classes of smart pointers:

(i) `auto_ptr/unique_ptr` - This kind of pointer is focussed on the first problem and follows the exclusive ownership pattern. It deallocates when it goes out of scope. `auto_ptr` was the original class created for this purpose that got deprecated in C++11 and was replaced by `unique_ptr`.

(ii) `shared_ptr` - This pointer is focussed on the second problem and follows the shared ownership pattern. It maintains a count of the number of owners the memory has and only deallocates when all the owners relinquish control.

(iii) `weak_ptr` -  This pointer takes a non-owning view on the object following the shared ownership pattern. IT can view the data but doesn't augment the count of the number of owners.


	#include <iostream>
	#include <memory>

	int main()
	{
		std::unique_ptr<int> u_p = std::make_unique<int>(5);
		std::cout << *u_p << std::endl;
		
		std::shared_ptr<int> s_p = std::make_shared<int>(6);
		std::cout << *s_p << std::endl;
		
		std::weak_ptr<int> w_p = s_p;
		std::shared_ptr<int> temp_p = w_p.lock();
		
		std::cout << *temp_p << std::endl;
		
		return 0;
	}

### Goal

By the end of these series, you should understand and be able to implement smart pointer classes.