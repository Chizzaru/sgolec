# SG-OLEC
Student Government Online Election 
Moore's Voting Algorithm


Given an integer array of length N. Check if there exists an integer which occurs more than floor(N/2) times. If there is no such element, print THERE IS NO MAJORITY ELEMENT.

Before going into the algorithm, let us see something interesting.

Let,

![image](https://user-images.githubusercontent.com/59724856/200457659-86a9983a-5c34-45db-89ed-12cbc2024ef9.png)


Let us eliminate two distinct numbers from the array. For this there are two possibilities :

Case 1: One number lies in majority elements and the other number lies in non-majority elements.

Case 2: Both the numbers lie in non-majority elements.

However, the occurrence of the majority elements contains the same number. So it is not possible to remove two distinct numbers from the occurrence of majority elements.

Case 1: One number lies in majority elements and the other number lies in non-majority elements.

![image](https://user-images.githubusercontent.com/59724856/200457835-f323433c-e429-46cb-9efd-128d814a8ecb.png)

After removing the elements, the majority element is still 3 as it occurs more than 6/2=3 times.

Therefore, there is no change in the majority element in this case.

Case 2: Both the numbers lie in non-majority elements.

![image](https://user-images.githubusercontent.com/59724856/200457919-656774e8-13c6-46a6-b075-347b627cbc8e.png)

After removing the elements, the majority element is still 3 as it occurs more than 6/2=3 times.

Therefore, there is no change in the majority element in this case.

The same idea is used in Moore’s Voting algorithm.

For this, we use two variables majority_element and count.

majority_element stores the majority element upto that instance and count stores its frequency upto that instance.

Initially, majority_element = input_array[0] and count = 1. Because input_array[0] has occurred once till this instance.

Now we traverse through the remaining elements. While traversing, if the array element is the same as the majority_element, we increment count by 1. If not, we decrement count by 1.

If count becomes 0 at any instance, we change the majority_element to the input_array element accessed at that instance and change count to 1.

The majority_element which we obtain after traversing all the input_array elements is expected to be the majority element of the complete array.

To find out if the element is actually the majority_element, we need to traverse again through all the input_array elements and count the frequency of majority_element in the array. If the frequency of the majority_element is greater than N/2, it is said to be the majority element.

If not, there is no majority element in the input_array.

Example:

![image](https://user-images.githubusercontent.com/59724856/200458124-820d4593-6aea-43f2-86e8-8fec85317ef1.png)

Initially,

![image](https://user-images.githubusercontent.com/59724856/200458173-f5e38ce1-f5b6-490d-b111-c9c4c7fca513.png)

input_array[i] != majority_element. So, count should be decremented by 1.

![image](https://user-images.githubusercontent.com/59724856/200458243-608b9542-da8a-4f38-8ae6-e7c95062a934.png)

Since count = 0, majority_element = input_array[i] and count = 1.

![image](https://user-images.githubusercontent.com/59724856/200458321-e31e4793-e485-45c2-8fff-fb06292cb389.png)

 input_array[i] != majority_element. So, count should be decremented by 1.
 
![image](https://user-images.githubusercontent.com/59724856/200460768-1799fd49-8ec9-445b-afc3-88abb7832273.png)

Since count = 0, majority_element = input_array[i] and count = 1.

![image](https://user-images.githubusercontent.com/59724856/200460722-7c82aea2-73ce-47e5-ba50-c6ecb7467270.png)

input_array[i] != majority_element. So, count should be decremented by 1.

![image](https://user-images.githubusercontent.com/59724856/200460541-41726fc4-12a9-428c-b80b-5fa0916ddd46.png)

Since count = 0, majority_element = input_array[i] and count = 1.

![image](https://user-images.githubusercontent.com/59724856/200460490-2caa37ba-7a76-4d6d-879a-52ab6a15d21e.png)

input_array[i] != majority_element. So, count should be decremented by 1.

![image](https://user-images.githubusercontent.com/59724856/200459407-674f52a2-395c-4c5b-87a3-db61a31f7cbe.png)

Since count = 0, majority_element = input_array[i] and count = 1.

![image](https://user-images.githubusercontent.com/59724856/200459356-2cd0fac7-29a4-4a5e-81a3-2f7e9ea1692e.png)

input_array[i] == majority_element. So, count should be incremented by 1.

![image](https://user-images.githubusercontent.com/59724856/200460096-3dcb5456-6e13-4c10-8be4-94585fd2a368.png)

![image](https://user-images.githubusercontent.com/59724856/200460073-18554eb5-6228-48d2-8c1c-45ebac85a938.png)

input_array[i] != majority_element. So, count should be decremented by 1.

![image](https://user-images.githubusercontent.com/59724856/200459255-93056567-18a2-47a3-9982-d2245d91977d.png)

![image](https://user-images.githubusercontent.com/59724856/200459225-98ba2e22-f96d-4b1b-9f22-2ba0f95d5467.png)

input_array[i] == majority_element. So, count should be incremented by 1.

![image](https://user-images.githubusercontent.com/59724856/200459189-23845b50-48c7-4b42-a720-1a32c1685b27.png)

After traversing all the elements,

![image](https://user-images.githubusercontent.com/59724856/200459165-b3f3aebe-84e6-408e-ab29-47c847dc4183.png)

Now lets count the occurrence of majority_element in input_array.

![image](https://user-images.githubusercontent.com/59724856/200459018-50a8fbcb-9854-4710-ade9-cd7d966a3368.png)

![image](https://user-images.githubusercontent.com/59724856/200459045-91c464a3-adb3-4111-83b0-6284bbbb5d3f.png)

![image](https://user-images.githubusercontent.com/59724856/200459077-aca004bf-61d9-4d38-add1-938baea9427c.png)


Source : https://www.programming9.com/tutorials/competitive-programming/428-moore-s-voting-algorithm#python
