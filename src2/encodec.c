#include <stdlib.h>
#include <unistd.h>

#include "util.h"
#include "dl_help.h"
#include "encodec.h"
#include "frame_buffer.h"

struct output_object *encodec_init(void)
{
	int ret;
	struct encodec_ops *dev_ops;
	struct output_object *output_obj;

	output_obj = calloc(1, sizeof(struct output_object));

	dev_ops = (struct encodec_ops *)load_lib_data("src2/encodec/sdl_output/libsdl_output.so", "dev_ops");

	if(!dev_ops)
	{
		char path_tmp[255];
		getcwd(path_tmp, 255);
		log_error("load libsdl_output.so fail. dir:%s\n", path_tmp);
		exit(-1);
	}

	ret = dev_ops->init(output_obj);
	if(ret == 0)
	{
		output_obj->ops = dev_ops;
	}else{
		log_error("libsdl_output.so init fail.");
		exit(-1);
	}

	return output_obj;
}

int output_set_info(struct output_object *output_obj, struct fb_info *fb_info)
{
	struct encodec_ops *dev_ops;
	
	if(!output_obj)
		return -1;

	dev_ops = (struct encodec_ops *)output_obj->ops;
	if(dev_ops)
	{
		if(dev_ops->set_info)
			return dev_ops->set_info(output_obj, fb_info);
		else
			printf("output dev not find func:set_info\n");
	}

	return -1;
}

int output_map_fb(struct output_object *output_obj, int buf_id)
{
	struct encodec_ops *dev_ops;
	
	if(!output_obj)
		return -1;

	dev_ops = (struct encodec_ops *)output_obj->ops;
	if(dev_ops)
	{
		if(dev_ops->map_buffer)
			return dev_ops->map_buffer(output_obj, buf_id);
		else
			printf("output dev not find func:map_buffer\n");
	}

	return -1;
}

int output_get_fb(struct output_object *output_obj)
{
	struct encodec_ops *dev_ops;
	
	if(!output_obj)
		return -1;

	dev_ops = (struct encodec_ops *)output_obj->ops;
	if(dev_ops)
	{
		if(dev_ops->get_buffer)
			return dev_ops->get_buffer(output_obj);
		else
			printf("output dev not find func:get_buffer\n");
	}

	return -1;
}

int output_put_fb(struct output_object *output_obj, int buf_id)
{
	struct encodec_ops *dev_ops;
	
	if(!output_obj)
		return -1;

	dev_ops = (struct encodec_ops *)output_obj->ops;
	if(dev_ops)
	{
		if(dev_ops->put_buffer)
			return dev_ops->put_buffer(output_obj, buf_id);
		else
			printf("output dev not find func:put_buffer\n");
	}

	return -1;
}

int output_regist_event_callback(struct output_object *output_obj, void (* on_event)(struct output_object *obj))
{
	if(!output_obj)
		return -1;

	output_obj->on_event = on_event;

	return 0;
}

int output_main_loop(struct output_object *output_obj)
{
	struct encodec_ops *dev_ops;

	if(!output_obj)
		return -1;

	dev_ops = (struct encodec_ops *)output_obj->ops;
	if(dev_ops)
	{
		if(dev_ops->event_loop)
			return dev_ops->event_loop(output_obj);
		else
			printf("output dev not find func:event_loop\n");
	}

	return -1;
}