# UI elements
A basic implementation of various ui elements using python and pygame

For now the only ui elements i have implemented are the label and the button
However i'll be coming back to this project and add a bunch of ui elements in the future, like :

1. Radiobutton
2.Entry box
3. Color picker
4. popup message box
5. breadcrumbs
6. menu
7. menubutton
8. file selector
9. check button
10. progress bar


## Button

![buttonAnatomy](https://github.com/user-attachments/assets/3aeac59c-1bb5-4c92-b971-8ca9220d6d34)

As you can see above these are some of the properties of the button i made using pygame.
I made the Button class take in a Button Style class which contains all possible alterable properties of a button such as : 

1. Padding
2. Font style
3. Background color
4. Foreground color
5. Font size
6. Hover effects (has to be coded if different)
7. Anti - Aliasing
8. Wrap length (move to next line when length of font exceed this variable)
9. Border

I will continuously add more and more properties each time i visit this project.

## Label

Next we have a label. It is just the same as the button in terms of font properties.
However it only dosent have a background rect and is only used to display text.

You can change any property of the label in the code by using the function:

>  Label.change( "<Property>", "<Value>") 

The alterable properties are mentioned in the _Label Style_ class

Thats it for now. See you next time :P
