package cloud.provider;

import javax.xml.ws.Endpoint;

public class Provider {

    private static final String URL = "http://localhost:9000/backup";

    public static void main(String[] args) {
        Backup cloud_backup = new Backup();
        System.out.println("Publishing Cloud Backup Service");
        Endpoint.publish(URL, cloud_backup);
        System.out.println("Cloud Backup Published");
    }
}