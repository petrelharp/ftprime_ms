/* Hello. You've ended up in here unexpectedly, and it's not very nice.
 * This code is awful, and I apologise. It's a mixture of automatically
 * generated code that illustrated something slightly different, and some hand
 * crafted asymptote. It doesn't make a lot of sense, and has been hacked in
 * all sorts of ways. 
 */
  
size(0,0);
defaultpen(fontsize(8pt));
unitsize(1cm);

/* TODO. These node assigments here have all been jumbled up and need to be fixed up. */
pen node_0 = rgb("875373");
pen node_1 = rgb("6AA944");
pen node_2 = rgb("C54C3C");
pen node_3 = rgb("B061D0");
pen node_4 = rgb("4A907F");
pen node_5 = rgb("6F84BD");

path mutation_marker = scale(0.03) * polygon(6);
pen mutation_fill = red;
path site_marker = scale(0.125) * polygon(4);
pen site_fill = 0.5 * white;
real total_width = 16.0;
real top_line = 5.5;
real mutation_header_y = 3;

draw((0,0)--(0,top_line)--(total_width,top_line)--(total_width,0)--cycle);
draw((6,0)--(6,top_line));
draw((8,0)--(8,top_line));
draw((0,2.5)--(6,2.5));

label('\\textbf{Tree topologies and mutations}', (0, top_line), SE);
label('\\textbf{Nodes}', (7.5, top_line), SW);
label('\\textbf{Edges}', (10.7, top_line), SW);
label('\\textbf{Sites}', (14, top_line), SW);
label('\\textbf{Mutations}', (14, mutation_header_y), SW);
label('\\textbf{Intervals}', (0, 2.5), SE);

real banner_height = 0.375;
real site_box_x = 12;
draw((site_box_x, 0)--(site_box_x, top_line));
draw((6, top_line - banner_height)--(total_width, top_line - banner_height));
draw((site_box_x, mutation_header_y)--(total_width, mutation_header_y));
draw((site_box_x, mutation_header_y - banner_height)--
    (total_width, mutation_header_y - banner_height));
/* draw((15.5, 0)--(15.5, top_line)); */

label('\\textbf{Encoded Tree Sequence}', (12, 6));
/* draw((0.5, 5.9)--(0.5, 6.1)); */

/* Draw the coordinate scale */
real y = -0.5;
real tick_top = y + 0.1;
real tick_bot = y - 0.1;

label('Genomic position', (3.0, y - 0.5));
draw((0.5, y)--(5.5, y));
label('$0$', (0.5, tick_bot), S);
label('$5$', (3.0, tick_bot), S);
label('$10$', (5.5, tick_bot), S);
draw((0.5, tick_top)--(0.5, tick_bot));
draw((3.0, tick_top)--(3.0, tick_bot));
draw((5.5, tick_top)--(5.5, tick_bot));

real x = 1.75;
label("Site 0", (x, tick_top), N);
filldraw(shift(x, y) * site_marker, site_fill);
real x = 4.25;
label("Site 1", (x, tick_top), N);
filldraw(shift(x, y) * site_marker, site_fill);
tick_top = y + 0.05;
tick_bot = y - 0.05;
for (real x = 1.0; x < 6; x += 0.5) {
    draw((x, tick_top)--(x, tick_bot));
}

/* Draw time scale */
real time_scale_x = -0.5;
real time_scale_bot = 3.5;
real y = time_scale_bot;
real eps = 0.05;
draw((time_scale_x - eps, y)--(time_scale_x + eps, y));
label("0", (time_scale_x - eps, y), W);
y += 0.65;
draw((time_scale_x - eps, y)--(time_scale_x + eps, y));
label("1", (time_scale_x - eps, y), W);
y += 0.65;
draw((time_scale_x - eps, y)--(time_scale_x + eps, y));
label("2", (time_scale_x - eps, y), W);
real time_scale_top = y;
draw((time_scale_x, time_scale_top)--(time_scale_x, time_scale_bot));
y = time_scale_top - (time_scale_top - time_scale_bot) / 2;
label(rotate(90) * "Time before present", (time_scale_x - 0.5, y), W);

picture state7;
unitsize(state7, 1cm);
size(state7, 6, 5);

real y = -5.5;
draw(state7, (0.5,y)--(5.5,y), black + 1);
dot(state7, (0.5,y));
dot(state7, (5.5,y), filltype=FillDraw(white));
y = y + 0.25;
draw(state7, '$1$', (2.75, y), e=roundbox, FillDraw(node_2));
draw(state7, (2.9, y)--(3.1, y), EndArrow(size=1mm));
draw(state7, '$3$', (3.25, y), e=roundbox, FillDraw(node_4));

y = -6.0;
draw(state7, (0.5,y)--(5.5,y), black + 1);
dot(state7, (0.5,y));
dot(state7, (5.5,y), filltype=FillDraw(white));
y = y + 0.25;
draw(state7, '$3$', (2.75, y), e=roundbox, FillDraw(node_4));
draw(state7, (2.9, y)--(3.1, y), EndArrow(size=1mm));
draw(state7, '$4$', (3.25, y), e=roundbox, FillDraw(node_5));

y = -6.5;
draw(state7, (0.5,y)--(3.0,y), black + 1);
dot(state7, (0.5,y));
dot(state7, (3.0,y), filltype=FillDraw(white));
y = y + 0.25;
draw(state7, '$0$', (1.5, y), e=roundbox, FillDraw(node_3));
draw(state7, (1.65, y)--(1.85, y), EndArrow(size=1mm));
draw(state7, '$3$', (2.0, y), e=roundbox, FillDraw(node_4));

y = -7.0;
draw(state7, (0.5,y)--(3.0,y), black + 1);
dot(state7, (0.5,y));
dot(state7, (3.0,y), filltype=FillDraw(white));
y = y + 0.25;
draw(state7, '$2$', (1.5, y), e=roundbox, FillDraw(node_1));
draw(state7, (1.65, y)--(1.85, y), EndArrow(size=1mm));
draw(state7, '$4$', (2.0, y), e=roundbox, FillDraw(node_5));

y = -6.5;
draw(state7, (3.0,y)--(5.5,y), black + 1);
dot(state7, (3.0,y));
dot(state7, (5.5,y), filltype=FillDraw(white));
y = y + 0.25;
draw(state7, '$2$', (4.0, y), e=roundbox, FillDraw(node_1));
draw(state7, (4.15, y)--(4.35, y), EndArrow(size=1mm));
draw(state7, '$3$', (4.5, y), e=roundbox, FillDraw(node_4));

y = -7.0;
draw(state7, (3.0,y)--(5.5,y), black + 1);
dot(state7, (3.0,y));
dot(state7, (5.5,y), filltype=FillDraw(white));
y = y + 0.25;
draw(state7, '$0$', (4.0, y), e=roundbox, FillDraw(node_3));
draw(state7, (4.15, y)--(4.35, y), EndArrow(size=1mm));
draw(state7, '$4$', (4.5, y), e=roundbox, FillDraw(node_5));

real state_y = -0.2;
picture state7_tree0;
unitsize(state7_tree0, 2.5cm);
draw(state7_tree0, (0.625, 0.3)--(0.5, 0.0), solid);
draw(state7_tree0, (0.625, 0.3)--(0.75, 0.0), solid);
draw(state7_tree0, (0.4375, 0.6)--(0.25, 0.0), solid);
draw(state7_tree0, (0.4375, 0.6)--(0.625, 0.3), solid);
draw(state7_tree0, '$2$', (0.25, 0.0), e=roundbox, FillDraw(node_1));
draw(state7_tree0, '$1$', (0.5, 0.0), e=roundbox, FillDraw(node_2));
draw(state7_tree0, '$0$', (0.75, 0.0), e=roundbox, FillDraw(node_3));
draw(state7_tree0, '$3$', (0.625, 0.3), e=roundbox, FillDraw(node_4));
draw(state7_tree0, '$4$', (0.4375, 0.6), e=roundbox, FillDraw(node_5));
label(state7_tree0, 'T', (0.25, state_y));
label(state7_tree0, 'A', (0.5, state_y));
label(state7_tree0, 'A', (0.75, state_y));

/* add mutation above node 2  */
pair x1 = (0.25, 0.0);
pair x2 = (0.4375, 0.6);
pair mid = x1 - (x1 - x2) / 2;
label(state7_tree0, '$0$', mid, W);
filldraw(state7_tree0, shift(mid) * mutation_marker, mutation_fill);
add(state7, state7_tree0.fit(), (1.5,-4.75), N);

picture state7_tree2;
unitsize(state7_tree2, 2.5cm);
draw(state7_tree2, (0.625, 0.3)--(0.5, 0.0), solid);
draw(state7_tree2, (0.625, 0.3)--(0.75, 0.0), solid);
draw(state7_tree2, (0.4375, 0.6)--(0.25, 0.0), solid);
draw(state7_tree2, (0.4375, 0.6)--(0.625, 0.3), solid);
draw(state7_tree2, '$0$', (0.25, 0.0), e=roundbox, FillDraw(node_3));
draw(state7_tree2, '$1$', (0.5, 0.0), e=roundbox, FillDraw(node_2));
draw(state7_tree2, '$2$', (0.75, 0.0), e=roundbox, FillDraw(node_1));
draw(state7_tree2, '$3$', (0.625, 0.3), e=roundbox, FillDraw(node_4));
draw(state7_tree2, '$4$', (0.4375, 0.6), e=roundbox, FillDraw(node_5));
label(state7_tree2, 'G', (0.25, state_y));
label(state7_tree2, 'C', (0.5, state_y));
label(state7_tree2, 'G', (0.75, state_y));

/* add mutation above node 3  */
x1 = (0.625, 0.3);
x2 = (0.4375, 0.6);
mid = x1 - (x1 - x2) / 2;
label(state7_tree2, '$1$', mid, E);
filldraw(state7_tree2, shift(mid) * mutation_marker, mutation_fill);
/* add mutation above node 1  */
x1 = (0.5, 0.0);
x2 = (0.625, 0.3);
mid = x1 - (x1 - x2) / 2;
label(state7_tree2, '$2$', mid, W);
filldraw(state7_tree2, shift(mid) * mutation_marker, mutation_fill);

add(state7, state7_tree2.fit(), (4.5,-4.75), N);

add(currentpicture, state7.fit(), (0,7.5));

label('ID', (6.5, 5.0), S, fontsize(6));
label('Time', (7.45, 5.0), S, fontsize(6));
label('Left', (8.5, 5.0), S, fontsize(6));
label('Right', (9.45, 5.0), S, fontsize(6));
label('Child', (10.399999999999999, 5.0), S, fontsize(6));
label('Parent', (11.349999999999998, 5.0), S, fontsize(6));

real site_id_x = 12.5;
real site_position_x = 13.5;
real site_ancestral_x = 14.8;
label('ID', (site_id_x, 5.0), S, fontsize(6));
label('Position', (site_position_x, 5.0), S, fontsize(6));
label('Ancestral', (site_ancestral_x, 5.0), S, fontsize(6));

real mutation_id_x = site_id_x;
real mutation_site_x = site_position_x;
real mutation_node_x = mutation_site_x + 1.0;
real mutation_derived_x = mutation_node_x + 1;
mutation_header_y -= 0.5;
label('ID', (mutation_id_x, mutation_header_y), S, fontsize(6));
label('Site', (mutation_site_x, mutation_header_y), S, fontsize(6));
label('Node', (mutation_node_x, mutation_header_y), S, fontsize(6));
label('Derived', (mutation_derived_x, mutation_header_y), S, fontsize(6));

/* Edges */
label('$0$', (8.5, 4.5));
label('$10$', (9.45, 4.5));
label('$1$', (10.399999999999999, 4.5));
label('$3$', (11.349999999999998, 4.5));
label('$0$', (8.5, 4.0));
label('$10$', (9.45, 4.0));
label('$3$', (10.399999999999999, 4.0));
label('$4$', (11.349999999999998, 4.0));
label('$0$', (8.5, 3.5));
label('$5$', (9.45, 3.5));
label('$0$', (10.399999999999999, 3.5));
label('$3$', (11.349999999999998, 3.5));
label('$0$', (8.5, 3.0));
label('$5$', (9.45, 3.0));
label('$2$', (10.399999999999999, 3.0));
label('$4$', (11.349999999999998, 3.0));
label('$5$', (8.5, 2.5));
label('$10$', (9.45, 2.5));
label('$2$', (10.399999999999999, 2.5));
label('$3$', (11.349999999999998, 2.5));
label('$5$', (8.5, 2.0));
label('$10$', (9.45, 2.0));
label('$0$', (10.399999999999999, 2.0));
label('$4$', (11.349999999999998, 2.0));

/* Nodes */
label('$0$', (6.5, 4.5));
label('$0.0$', (7.45, 4.5));
label('$1$', (6.5, 4.0));
label('$0.0$', (7.45, 4.0));
label('$2$', (6.5, 3.5));
label('$0.0$', (7.45, 3.5));
label('$3$', (6.5, 3.0));
label('$1.0$', (7.45, 3.0));
label('$4$', (6.5, 2.5));
label('$2.0$', (7.45, 2.5));

/* Sites */
y = 4.5;
label('$0$', (site_id_x, y));
label('$2.5$', (site_position_x, y));
label('A', (site_ancestral_x, y));
y = 4.0;
label('$1$', (site_id_x, y));
label('$7.5$', (site_position_x, y));
label('G', (site_ancestral_x, y));

/* Mutations */
y = mutation_header_y - 0.5;
label('$0$', (mutation_id_x, y));
label('$0$', (mutation_site_x, y));
label('$2$', (mutation_node_x, y));
label('T', (mutation_derived_x, y));

y -= 0.5;
label('$1$', (mutation_id_x, y));
label('$1$', (mutation_site_x, y));
label('$3$', (mutation_node_x, y));
label('C', (mutation_derived_x, y));

y -= 0.5;
label('$2$', (mutation_id_x, y));
label('$1$', (mutation_site_x, y));
label('$1$', (mutation_node_x, y));
label('G', (mutation_derived_x, y));

