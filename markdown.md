## Enable Math

1. Math rendering is disabled by default, to enable it, check on the *Enable Math* option in *Preferences* > *General* > *All Documents*:.

2. Make sure you've connected to the internet.

   The Math rendering is powered by [MathJax](http://www.mathjax.org), the resources such as fonts are all online, thus the internet connection is needed for it to work.
   
3. For Users in mainland China

   Users in mainland China, if the Math option doesn't work for you, try if you can visit [MathJax](http://www.mathjax.org) without VPN connected. If you can't, maybe it's blocked by the Great Firewall of China. Try connect to a VPN, climb over the wall, then the Math rendering should work.

### Known issues of Math option

1. It makes the Preview blink and blink again whenever typing.

   Math support is a good addition, except that it makes the Preview blink and blink again whenever typing, as it needs to refresh the whole typesetting.

2. It makes the Right View always scroll to top whenever typing.

 
That's why I make it disabled by default. I suggest only enable it when you write Math Formulas, or better, only enable it when you export document to HTML which contains Math Formulas, when you are writing, disable it.


## Block level vs Inline level

Use double US dollors sign pair for Block level Math formula, and three US dollors sign pair for Inline Level.

For example this is a Block level $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}$$ formula, and this is an inline Level $$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}$$$ formula.


## The Math Syntax

The syntax is the same as [**Tex**](http://en.wikipedia.org/wiki/TeX), expect one thing:

Because the characters such as \ and _ and * and so on have special meanings in Markdown language, you need to add an extra \ character before them to escape them to make the Math renders correctly.

For example in TeX syntax it starts with \[ but here you need to add an extra \ to escape it, thus \\[

And so on… Luckily you don't have to escape every \ characters, normally escape the beginning \[ and ending \] is enough, and perhaps \\ to \\\. 

#### The Quadratic Formula

$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}$$

#### The Lorenz Equations

\\[\begin{aligned}
\dot{x} & = \sigma(y-x) \\\
\dot{y} & = \rho x - y - xz \\\
\dot{z} & = -\beta z + xy
\end{aligned} \\]

#### The Cauchy-Schwarz Inequality

\\[ \left( \sum\_{k=1}^n a_k b_k \right)^2 \leq \left( \sum\_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right) \\]

#### A Cross Product Formula

\\[\mathbf{V}\_1 \times \mathbf{V}\_2 =  \begin{vmatrix}
\mathbf{i} & \mathbf{j} & \mathbf{k} \\\
\frac{\partial X}{\partial u} &  \frac{\partial Y}{\partial u} & 0 \\\
\frac{\partial X}{\partial v} &  \frac{\partial Y}{\partial v} & 0
\end{vmatrix} \\]

#### The probability of getting $$$k$$$ heads when flipping $$$n$$$ coins is

\\[P(E) = {n \choose k} p^k (1-p)^{ n-k} \\]

#### An Identity of Ramanujan

\\[ \frac{1}{\Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{\frac25 \pi}} =
1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {1+\frac{e^{-6\pi}}
{1+\frac{e^{-8\pi}} {1+\ldots} } } } \\]

#### Maxwell’s Equations

\\[  \begin{aligned}
\nabla \times \vec{\mathbf{B}} -\, \frac1c\, \frac{\partial\vec{\mathbf{E}}}{\partial t} & = \frac{4\pi}{c}\vec{\mathbf{j}} \\   \nabla \cdot \vec{\mathbf{E}} & = 4 \pi \rho \\
\nabla \times \vec{\mathbf{E}}\, +\, \frac1c\, \frac{\partial\vec{\mathbf{B}}}{\partial t} & = \vec{\mathbf{0}} \\
\nabla \cdot \vec{\mathbf{B}} & = 0 \end{aligned}
\\]

#### A Rogers-Ramanujan Identity

\\[  1 +  \frac{q^2}{(1-q)}+\frac{q^6}{(1-q)(1-q^2)}+\cdots =
\prod_{j=0}^{\infty}\frac{1}{(1-q^{5j+2})(1-q^{5j+3})},
\quad\quad \text{for $|q|<1$}. \\]