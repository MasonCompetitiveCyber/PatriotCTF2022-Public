package com.patriotctf.RCE;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
// import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@Controller
public class RceApplication extends SpringBootServletInitializer{

	 @Override
    protected SpringApplicationBuilder configure (SpringApplicationBuilder builder) {
        return builder.sources(RceApplication.class);
    }

	public static void main(String[] args) {
		SpringApplication.run(RceApplication.class, args);
	}

	@GetMapping("/")
	public String index(){
		return "index";
		

		}

}
